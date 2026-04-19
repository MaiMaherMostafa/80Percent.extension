# -*- coding: utf-8 -*-
from pyrevit import revit, DB, script, forms
import clr

clr.AddReference("Microsoft.Office.Interop.Excel")
from Microsoft.Office.Interop import Excel

doc = revit.doc
output = script.get_output()

# -------------------------------------------------------
# PICK EXCEL FILE
# -------------------------------------------------------

excel_path = forms.pick_file(file_ext='xlsx', title='Select Excel File')
if not excel_path:
    script.exit()

# -------------------------------------------------------
# READ EXCEL
# -------------------------------------------------------

excel = Excel.ApplicationClass()
excel.Visible = False
workbook = excel.Workbooks.Open(excel_path)
sheet = workbook.ActiveSheet

views_data = []

row = 2
while True:
    view_name = sheet.Cells[row, 1].Value2
    if not view_name:
        break

    scale = int(sheet.Cells[row, 2].Value2)
    level_name = str(sheet.Cells[row, 3].Value2)
    make_sheet = str(sheet.Cells[row, 4].Value2).upper() == "YES"
    sheet_number = str(sheet.Cells[row, 5].Value2)
    template_name = sheet.Cells[row, 6].Value2  # NEW

    views_data.append(
        (view_name, scale, level_name, make_sheet, sheet_number, template_name)
    )
    row += 1

workbook.Close(False)
excel.Quit()

# -------------------------------------------------------
# COLLECT REVIT DATA
# -------------------------------------------------------

levels = {lvl.Name: lvl for lvl in DB.FilteredElementCollector(doc).OfClass(DB.Level)}
existing_views = {v.Name: v for v in DB.FilteredElementCollector(doc).OfClass(DB.ViewPlan)}
existing_sheets = {s.SheetNumber: s for s in DB.FilteredElementCollector(doc).OfClass(DB.ViewSheet)}

# View Templates
templates = {
    v.Name: v
    for v in DB.FilteredElementCollector(doc).OfClass(DB.View)
    if v.IsTemplate
}

# Structural Plan Type
view_family_types = DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType)
struct_plan_type = next(v for v in view_family_types if v.ViewFamily == DB.ViewFamily.StructuralPlan)

# Title Block
titleblock = DB.FilteredElementCollector(doc)\
    .OfCategory(DB.BuiltInCategory.OST_TitleBlocks)\
    .WhereElementIsElementType()\
    .FirstElement()

if not titleblock:
    forms.alert("No title block found.", exitscript=True)

# -------------------------------------------------------
# CREATE VIEWS / APPLY TEMPLATES / CREATE SHEETS
# -------------------------------------------------------

with DB.Transaction(doc, "Create Views, Sheets, and Apply Templates") as t:
    t.Start()

    for view_name, scale, level_name, make_sheet, sheet_number, template_name in views_data:

        # -------- VIEW --------
        if view_name in existing_views:
            view = existing_views[view_name]
            output.print_md("✅ View exists: **{}**".format(view_name))
        else:
            level = levels.get(level_name)
            if not level:
                output.print_md("❌ Level not found: **{}**".format(level_name))
                continue

            view = DB.ViewPlan.Create(doc, struct_plan_type.Id, level.Id)
            view.Name = view_name
            view.Scale = scale
            output.print_md("🆕 Created view: **{}**".format(view_name))

        # -------- APPLY VIEW TEMPLATE --------
        if template_name:
            template = templates.get(template_name)
            if template:
                view.ViewTemplateId = template.Id
                output.print_md("🎯 Applied template: **{}**".format(template_name))
            else:
                output.print_md("⚠️ Template not found: **{}**".format(template_name))

        # -------- SHEET --------
        if make_sheet:
            sheet = existing_sheets.get(sheet_number)
            if not sheet:
                sheet = DB.ViewSheet.Create(doc, titleblock.Id)
                sheet.SheetNumber = sheet_number
                sheet.Name = view_name
                output.print_md("🆕 Created sheet: **{}**".format(sheet_number))

            # -------- PLACE VIEW ON SHEET (FIXED) --------
            if DB.Viewport.CanAddViewToSheet(doc, sheet.Id, view.Id):

                # Get title block instance on the sheet
                titleblocks_on_sheet = [
                    el for el in DB.FilteredElementCollector(doc, sheet.Id)
                    .OfCategory(DB.BuiltInCategory.OST_TitleBlocks)
                    .WhereElementIsNotElementType()
                ]

                if titleblocks_on_sheet:
                    tb = titleblocks_on_sheet[0]
                    bbox = tb.get_BoundingBox(sheet)

                    center = DB.XYZ(
                        (bbox.Min.X + bbox.Max.X - 0.5) / 2,
                        (bbox.Min.Y + bbox.Max.Y) / 2,
                        0
                    )
                else:
                    # Safe fallback
                    center = DB.XYZ(1, 1, 0)

                DB.Viewport.Create(doc, sheet.Id, view.Id, center)
                output.print_md("✅ View placed correctly on sheet")

    t.Commit()

output.print_md("🎉 **Views, sheets, and templates processed successfully**")