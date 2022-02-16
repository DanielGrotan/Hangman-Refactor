from application.settings import Settings
from application.window import ApplicationWindow
from main_menu.menu import MainMenu


def main():
    settings = Settings(settings_path="settings.json")
    application_window = ApplicationWindow(settings, application_name="Hangman")

    MainMenu(settings, application_window).start()


if __name__ == "__main__":
    main()
