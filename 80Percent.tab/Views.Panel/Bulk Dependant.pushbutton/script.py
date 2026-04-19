# -*- coding: utf-8 -*-
# pyRevit script: Pick Plan Views (Floor, Ceiling, Structural)
# and Duplicate as Dependent with Suffix

from pyrevit import revit, forms
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    ViewPlan,
    ViewType,
    ViewDuplicateOption
)

doc = revit.doc

# ---------------------------------------------------------------------
# Collect all plan views (Floor, Ceiling, Structural – no templates)
# ---------------------------------------------------------------------
all_plans = [
    v for v in FilteredElementCollector(doc).OfClass(ViewPlan)
    if not v.IsTemplate
    and v.ViewType in [
        ViewType.FloorPlan,
        ViewType.CeilingPlan,
        ViewType.EngineeringPlan
    ]
]

if not all_plans:
    forms.alert("No plan views found in this project.", exitscript=True)

# ---------------------------------------------------------------------
# Pick multiple views from list
# ---------------------------------------------------------------------
selected_views = forms.SelectFromList.show(
    sorted(all_plans, key=lambda x: x.Name),
    name_attr="Name",
    title="Select Plan Views to Duplicate",
    multiselect=True
)

if not selected_views:
    forms.alert("No views selected.", exitscript=True)

# ---------------------------------------------------------------------
# User input: number of dependents
# ---------------------------------------------------------------------
num_duplicates = forms.ask_for_string(
    prompt="Enter number of dependent views per plan:",
    title="Duplicate As Dependent",
    default="2"
)

if not num_duplicates or not num_duplicates.isdigit():
    forms.alert("Invalid number entered.", exitscript=True)

num_duplicates = int(num_duplicates)

# ---------------------------------------------------------------------
# User input: suffix
# ---------------------------------------------------------------------
suffix = forms.ask_for_string(
    prompt='Enter view name suffix (e.g. "PART"):',
    title="Duplicate As Dependent",
    default="PART"
)

if not suffix:
    forms.alert("Suffix cannot be empty.", exitscript=True)

# ---------------------------------------------------------------------
# Duplicate views as dependents
# ---------------------------------------------------------------------
failed_views = []

with revit.Transaction("Duplicate Plan Views As Dependent"):
    for view in selected_views:
        for i in range(1, num_duplicates + 1):
            try:
                new_view_id = view.Duplicate(
                    ViewDuplicateOption.AsDependent
                )
                new_view = doc.GetElement(new_view_id)

                # Suffix naming
                new_view.Name = "{} - {} {}".format(
                    view.Name, suffix, i
                )

            except Exception:
                failed_views.append(view.Name)
                break

# ---------------------------------------------------------------------
# Result message
# ---------------------------------------------------------------------
msg = "✅ Dependent plan views created successfully."

if failed_views:
    msg += (
        "\n\n⚠️ Some views could not be duplicated as dependents:\n"
        + "\n".join(set(failed_views))
    )

forms.alert(msg, title="Finished")