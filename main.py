from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from google import genai
import threading

client = genai.Client(api_key="AQ.Ab8RN6K_IqD3kQtyVXkIntMebE1N678kSM5pAwSvSfw5d6Qlag")

class VirtualOikikMobile(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        self.output_label = Label(
            text="[Virtual Oikik Mobile AI]\nAsk me anything!",
            size_hint_y=0.6,
            halign='center',
            valign='middle',
            markup=True
        )
        self.output_label.bind(size=self.output_label.setter('text_size'))
        self.add_widget(self.output_label)

        self.user_input = TextInput(
            text='',
            hint_text='Type your query here...',
            size_hint_y=0.15,
            multiline=False
        )
        self.add_widget(self.user_input)

        self.submit_btn = Button(
            text='Ask Gemini',
            size_hint_y=0.15,
            background_color=(0.1, 0.5, 0.8, 1)
        )
        self.submit_btn.bind(on_press=self.send_to_gemini)
        self.add_widget(self.submit_btn)

    def send_to_gemini(self, instance):
        query = self.user_input.text.strip()
        if not query:
            return
        
        self.output_label.text = "Thinking..."
        threading.Thread(target=self._query_thread, args=(query,)).start()

    def _query_thread(self, query):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=query,
            )
            result_text = response.text
        except Exception as e:
            result_text = f"Error: {str(e)}"
        
        # Schedule UI update back on the main thread safely
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: setattr(self.output_label, 'text', result_text))

class VirtualOikikApp(App):
    def build(self):
        return VirtualOikikMobile()

if __name__ == '__main__':
    VirtualOikikApp().run()
