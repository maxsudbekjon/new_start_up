from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from jnius import autoclass, JavaException
from android.permissions import request_permissions, Permission
#
# Android API
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
UsageStatsManager = autoclass('android.app.usage.UsageStatsManager')
System = autoclass('java.lang.System')

# Kuzatiladigan ilovalar
watched_apps = {
    "com.instagram.android": "Insstagram",
    "com.zhiliaoapp.musically": "TikTok",
    "org.telegram.messenger": "Telegram"
}


def get_foreground_app():
    """Hozirgi ochilgan ilovani aniqlash"""
    try:
        context = PythonActivity.mActivity.getApplicationContext()
        usm = context.getSystemService(Context.USAGE_STATS_SERVICE)

        if usm is None:
            return None, "❌ UsageStatsManager mavjud emas (Permission yo‘q)"

        end = System.currentTimeMillis()
        begin = end - 1000 * 10
        stats = usm.queryUsageStats(UsageStatsManager.INTERVAL_DAILY, begin, end)

        if not stats:
            return None, "⚠️ Usage stats bo‘sh (Permission berilmagan bo‘lishi mumkin)"

        recent_app = None
        last_time = 0

        for usage in stats.toArray():
            if usage.getLastTimeUsed() > last_time:
                last_time = usage.getLastTimeUsed()
                recent_app = usage.getPackageName()

        return recent_app, None

    except JavaException as e:
        return None, f"JavaException: {e}"
    except Exception as e:
        return None, f"Exception: {e}"


class MyApp(App):
    def build(self):
        # Permission olish
        request_permissions([Permission.PACKAGE_USAGE_STATS])

        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Ilovaga kirishga ruxsat berasizmi?", font_size=20)
        self.status_label = Label(text="", font_size=16)

        btn_yes = Button(text="Ha", font_size=18)
        btn_no = Button(text="Yo'q", font_size=18)

        btn_yes.bind(on_press=self.allow_access)
        btn_no.bind(on_press=self.deny_access)

        self.layout.add_widget(self.label)
        self.layout.add_widget(btn_yes)
        self.layout.add_widget(btn_no)
        self.layout.add_widget(self.status_label)

        return self.layout

    def allow_access(self, instance):
        self.label.text = "✅ Monitoring boshlandi"
        # Har 2 soniyada update bo‘lsin
        self.event = Clock.schedule_interval(self.update_status, 2)

    def deny_access(self, instance):
        self.label.text = "❌ Siz rad qildingiz. Ilova yopilmoqda..."
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 1)

    def update_status(self, dt):
        app, error = get_foreground_app()

        if error:
            self.status_label.text = error
            return

        if app in watched_apps:
            self.status_label.text = f"📱 {watched_apps[app]} ochildi"
        else:
            self.status_label.text = f"Hozirgi app: {app}" if app else "App aniqlanmadi"

    def on_stop(self):
        # Ilova yopilganda monitoringni to‘xtatish
        if hasattr(self, "event"):
            self.event.cancel()


if __name__ == "__main__":
    MyApp().run()
