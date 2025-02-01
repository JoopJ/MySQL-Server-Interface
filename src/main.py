
import core.event_system as event_sys
import core.app_state as app_state
import ui.windows.main_window as main_wdo
import ui.ui_components as ui_cmp

if __name__ == "__main__":
    # Initialize the EventSystem and UIComponents
    # storing the EventSystem in the UIComponents singleton
    event_system = event_sys.EventSystem()
    ui_cmp.UIComponents.initialize(event_system)
    ui_components = ui_cmp.UIComponents.get_instance()
    
    # Begin the application
    main_window = main_wdo.MainWindow(ui_components)
    app = app_state.AppState(ui_components, main_window)
    app.begin()
    
    main_window.mainloop()
    
    