from time import sleep
import uiautomation as auto


class Calc():
    def open_calc(self):
        # 打开计算器
        desktop = auto.PaneControl(Name='任务栏')
        # 点击任务栏
        desktop.Click()
        # Win+D ,显示桌面
        desktop.SendKeys('{Win}d')
        # Win+R ,打开运行界面,并输入calc,打开浏览器
        desktop.SendKeys('{Win}r')
        run_win = auto.WindowControl(Name='运行')
        run_win_edit = run_win.EditControl(ClassName='Edit', Name='打开(O):')
        run_win_edit.SendKeys("calc")
        run_win_ok = run_win.ButtonControl(ClassName="Button", Name='确定')
        run_win_ok.Click()
        sleep(3)

    def calc_auto(self):
        calc_win = auto.WindowControl(ClassName='ApplicationFrameWindow', Name="计算器")
        # 开始计算
        calc_five = calc_win.ButtonControl(Name='五')
        calc_five.Click()
        calc_five.Click()
        calc_mult = calc_win.ButtonControl(Name='乘以')
        calc_mult.Click()
        calc_one = calc_win.ButtonControl(Name='一')
        calc_one.Click()
        calc_three = calc_win.ButtonControl(Name='三')
        calc_three.Click()
        calc_four = calc_win.ButtonControl(Name='四')
        calc_four.Click()
        calc_equal = calc_win.ButtonControl(Name="等于")
        calc_equal.Click()
        sleep(3)
        calc_win_close_btn = calc_win.ButtonControl(AutomationId='Close')
        calc_win_close_btn.Click()


if __name__ == '__main__':
    calc = Calc()
    calc.open_calc()
    calc.calc_auto()