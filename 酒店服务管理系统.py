import windows_control
import database_control


def main():
   windows_control.int_login_windows()


if __name__ == '__main__':
    main()
    database_control.db.close()