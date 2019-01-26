import time, sys, keyboard
import gameselect, ui_scan, action_scan, clicker, time_report, screencap


def main_exec():
    gameparams = gameselect.gselect(sys.argv)

    board = ui_scan.init_board(gameparams)
    action_result = None

    actions = set()
    action_result = None

    while True:
        print('Start cycle')
        if action_result and action_result.requires_scan:
            time_report.start_report('scan sleep')
            time.sleep(0.4)
            time_report.end_report()

            time_report.start_report('screen grab')
            cap = screencap.grab(gameparams)
            time_report.end_report()

            if action_result.danger_actions \
                and ui_scan.game_over_scan(gameparams, cap, action_result.danger_actions):
                ui_scan.print_scan(board)
                print('Game over')
                return

            time_report.start_report('ui scan')
            ui_scan.scan(gameparams, board, cap)
            time_report.end_report()
            # ui_scan.print_scan(board)
            requires_scan = False

        time_report.start_report('action scan')
        actions = action_scan.scan(gameparams, board)
        time_report.end_report()
        # action_scan.print_actions(actions)

        if keyboard.is_pressed('q'):
            return

        time_report.start_report('action execution')
        action_result = clicker.process_actions(gameparams, actions)
        time_report.end_report()

        if len(actions) == 0:
            break

if __name__ == "__main__":
    main_exec()
