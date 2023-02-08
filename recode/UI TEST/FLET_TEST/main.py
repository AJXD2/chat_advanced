import flet as ft

def main(page: ft.Page):

    def addTask(p):
        checkBox = ft.Checkbox(value=False, on_change=deletecheck)
        checkBoxText = ft.Text(value=textField.value, width=350, color="WHITE", size=15)
        taskRow = ft.Row(controls=[checkBox, checkBoxText], alignment=ft.MainAxisAlignment.START)
        page.add(taskRow)
    page.window_width = 500
    page.window_height = 700
    textField = ft.TextField()
    addBtn = ft.ElevatedButton("Add", icon=ft.icons.ADD, on_click=addTask)
    


    
    entriesRow=ft.Row(controls=[textField, addBtn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    page.add(entriesRow)  

ft.app(target=main)