import flet as ft



class Todo(ft.UserControl):
    def build(self):
        self.input = ft.TextField(hint_text="What should be done?", expand=True)

        self.tasks = ft.Column()

        view = ft.Column(
            self,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                
                ft.Text(value="ToDos", 
                        style=ft.TextThemeStyle.HEADLINE_MEDIUM)
            ]
        )

        return view


def main(page: ft.Page):
    page.window_height = 600
    page.window_width = 400

    page.title = 'ToDo'

    page.update()
    page.add(Todo)

ft.app(target=main)