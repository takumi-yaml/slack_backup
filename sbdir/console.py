from sbdir.slack_backup import SlackBackup
import argparse

def main():
    sb = SlackBackup()

    # usageを書き足す
    parser = argparse.ArgumentParser(prog="slack_backup")
    
    parser.add_argument("file", metavar="<path>", help="make backup", default=sb.default_conf_path, nargs="?")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m","--mail", action="store_true",  help="mail to zip file your account")
    group.add_argument("--dry-run", action="store_true",  help="only print files that you're going to make and zip")
    group.add_argument("-i","--init", action="store_true", help="make bare config file")
    group.add_argument("--version", action="version", version="%(prog)s {}".format(sb.__version__) ,help="show version")
    
    args = parser.parse_args()


    print(args)

    if args.init:
        relpath = sb.makeBareConfig()
        print('conf file "{}" is made.'.format(relpath))
        return

    if "version" in args:
        print(sb.__version__)
        return
    
    sb.getConfig(args.file)

    if args.dry_run:
        sb.main(debug=True)
        sb.mail()
        return

    if args.mail:
        sb.main()
        sb.mail()
        return

    sb.main()


if __name__ == "__main__":
    main()
