<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Processing Columns..."
        Width="460"
        SizeToContent="Height"
        MinHeight="170"
        WindowStartupLocation="CenterScreen"
        ResizeMode="NoResize"
        ShowInTaskbar="False"
        WindowStyle="ToolWindow"
        Topmost="True"
        Background="#FFFFFFFF">

    <!-- LIGHT PURPLE THEME -->
    <Window.Resources>
        <SolidColorBrush x:Key="TextDark"     Color="#202020"/>
        <SolidColorBrush x:Key="BorderLight"  Color="#D0D0D0"/>

        <!-- Gradient Purple -->
        <LinearGradientBrush x:Key="PurpleGrad" StartPoint="0,0" EndPoint="0,1">
            <GradientStop Color="#d02ddb" Offset="0"/>
            <GradientStop Color="#b405c7" Offset="1"/>
        </LinearGradientBrush>

        <SolidColorBrush x:Key="PurpleHover"  Color="#F6A1FF"/>
        <SolidColorBrush x:Key="PurplePress"  Color="#C430D6"/>

        <!-- Text -->
        <Style TargetType="TextBlock">
            <Setter Property="Foreground" Value="{StaticResource TextDark}"/>
        </Style>

        <!-- BUTTON -->
        <Style TargetType="Button">
            <Setter Property="Background"     Value="{StaticResource PurpleGrad}"/>
            <Setter Property="Foreground"     Value="White"/>
            <Setter Property="BorderBrush"    Value="{StaticResource PurplePress}"/>
            <Setter Property="BorderThickness" Value="1.5"/>
            <Setter Property="Padding"        Value="6,3"/>
            <Setter Property="Cursor"         Value="Hand"/>
            <Setter Property="Template">
                <Setter.Value>
                    <ControlTemplate TargetType="Button">
                        <Border CornerRadius="4"
                                Background="{TemplateBinding Background}"
                                BorderBrush="{TemplateBinding BorderBrush}"
                                BorderThickness="{TemplateBinding BorderThickness}">
                            <ContentPresenter HorizontalAlignment="Center"
                                              VerticalAlignment="Center"/>
                        </Border>
                    </ControlTemplate>
                </Setter.Value>
            </Setter>
            <Style.Triggers>
                <Trigger Property="IsMouseOver" Value="True">
                    <Setter Property="Background" Value="{StaticResource PurpleHover}"/>
                </Trigger>
                <Trigger Property="IsPressed" Value="True">
                    <Setter Property="Background" Value="{StaticResource PurplePress}"/>
                </Trigger>
            </Style.Triggers>
        </Style>

        <!-- PROGRESSBAR -->
        <Style TargetType="ProgressBar">
            <Setter Property="Foreground" Value="{StaticResource PurpleGrad}"/>
            <Setter Property="Background" Value="#FFF0F0F0"/>
        </Style>

    </Window.Resources>

    <Grid Margin="14">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>

        <TextBlock x:Name="MsgLabel" Text="Please wait..." 
                   FontSize="14" Margin="0,0,0,8"/>

        <StackPanel Grid.Row="1" Orientation="Vertical">
            <ProgressBar x:Name="ProgBar" Height="20" Minimum="0" Maximum="100" Value="0"/>
            <TextBlock x:Name="PctLabel" Text="0%" HorizontalAlignment="Right" Margin="0,4,0,0"/>
        </StackPanel>

        <StackPanel Grid.Row="2" Orientation="Horizontal" HorizontalAlignment="Right" Margin="0,10,0,0">
            <Button x:Name="CancelBtn" Width="90" Margin="6" Content="Cancel"/>
        </StackPanel>

    </Grid>
</Window>