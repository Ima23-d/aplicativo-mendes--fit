import flet as ft 
import pandas as pd 
import time
import asyncio
import winsound

data = pd.read_csv('exercises.csv')
def gerar_plano_treino(sexo, nivel, doenca, altura, peso,objetivo):
    altura = float(altura)
    peso = float(peso)
    
    # Define um intervalo de altura e peso de 10 unidades para mais e para menos
    altura_min = altura - 0.15
    altura_max = altura + 0.15
    peso_min = peso - 15
    peso_max = peso + 15
    
    # Filtra o DataFrame baseado no sexo, nível, doença, intervalo de altura e peso fornecidos
    filtered_df = data[
        (data['sex'] == sexo) & 
        (data['obj'] == objetivo) &
        (data['level_1'] == nivel) & 
        ((data['doenca'].str.contains(doenca, na=False, case=False)) | (data['doenca'] == 'nenhuma')) & 
        (data['altura'].between(altura_min, altura_max)) &
        (data['peso'].between(peso_min, peso_max))
    ]
    
    # Verificação para depuração
    print("Dados filtrados:")
    print(filtered_df)
    
    # Agrupa os exercícios por parte do corpo
    plano = {}
    for part in ['braço', 'costas', 'abdômen', 'perna', 'peito', 'ombro', 'glúteo']:
        exercises = filtered_df[filtered_df['body_part'] == part]['exercise'].tolist()
        plano[part] = exercises[:6]  # Limita a 6 exercícios por parte do corpo
    
    return plano
# Função para gerar o plano de treino
# def gerar_plano_treino(sexo, nivel, doenca):
#     # Filtra o DataFrame baseado no sexo, nível e doença fornecidos
#     filtered_df = data[(data['sex'] == sexo) & (data['level_1'] == nivel) & (data['doenca'].str.contains(doenca, na=False))]
#     # Agrupa os exercícios por parte do corpo
#     plano = {}
#     for part in ['braço', 'costa', 'abdômen', 'perna', 'peito', 'ombro', 'glúteo']:
#         exercises = filtered_df[filtered_df['body_part'] == part]['exercise'].tolist()
#         plano[part] = exercises[:6]  # Limita a 6 exercícios por parte do corpo
#     return plano

# Função principal da aplicação

#nutrição 
plano_nutri = {} 
data_nutri = pd.read_csv('nutricao.csv')

def gerar_plano_nutricao(restricao, preferencia, vegano, doenca_alimentar):
    filtered_df_nutri = data_nutri[
        (data_nutri['restricao'].str.lower() == restricao.lower()) &
        (data_nutri['preferencia'].str.lower() == preferencia.lower()) &
        (data_nutri['vegano'].str.lower() == vegano.lower()) &
        (data_nutri['doença_alimentar'].str.lower() == doenca_alimentar.lower())
    ]

    print("Dados filtrados:")
    print(filtered_df_nutri)
    
    plano_nutri = {}
    dias_semana = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
    for dia in dias_semana:
        etapas = filtered_df_nutri[filtered_df_nutri['dias'].str.lower() == dia]['etapas'].tolist()
        etapas = filtered_df_nutri[filtered_df_nutri['dias'].str.lower() == dia]['etapas'].tolist()
        plano_nutri[dia] = etapas[:6]  # Limita a 6 alimentos por dia
    
    print("Plano Nutri:")
    print(plano_nutri)
    
    return plano_nutri
def main(page: ft.Page):
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window_width = 450
    page.window_height = 700
    page.bgcolor = "#03B403"
    page.title = "Mendes - Fit"

    altura = ft.TextField(label="Digite a sua altura(Ex: 1.68)", width=300, height=50, bgcolor="white", border_radius=20, border=None)
    peso = ft.TextField(label="Digite o seu peso(Ex: 65)", width=300, height=50, bgcolor="white", border_radius=20, border=None)
    sexo = ft.TextField(label="Digite o seu sexo(Ex: homem/mulher)", width=300, height=50, bgcolor="white", border_radius=20, border=None)
    nivel = ft.TextField(label="Nível de treino(Ex: básico/intermediário/avançado)", width=300, height=50, bgcolor="white", border_radius=20, border=None)
    doenca = ft.TextField(label="Possui alguma doença?(Ex: asma/nenhuma)", width=300, height=50, bgcolor="white", border_radius=20, border=None)
    objetivo = ft.TextField(label="Objetivo(Ex:estética/peso/saúde)", width=300, height=50, bgcolor="white", border_radius=20, border=None)
    #alimentação 
    
    #alimentação 
    restrição = ft.TextField(label="Possui alguma restrição alimentar?",width=300,height=50,bgcolor="white",border_radius=20,border=None)
    preferencia = ft.TextField(label="Preferencia em comida?",width=300,height=50,bgcolor="white",border_radius=20,border=None)
    vegano = ft.TextField(label="È vegano(a) ?",width=300,height=50,bgcolor="white",border_radius=20,border=None)
    doenca_alimentar = ft.TextField(label="Possui alguma doença alimentar?",width=300,height=50,bgcolor="white",border_radius=20,border=None)
  

    

    def show_exercise_details(page, exercise_name):
        row = data[data['exercise'] == exercise_name].iloc[0]
        gif = row['gif_img']
        
        time_text = ft.Text(value="00:00:00", size=40, offset=ft.Offset(x=0.7, y=0), color="white")

    # Criar um campo de entrada para o tempo desejado
        desired_time_input = ft.CupertinoTimerPicker(offset=ft.Offset(x=0.2, y=0), bgcolor="#05A805", width=300, height=50)
        start_time = 0
        running = False
        paused = False
        desired_time = 0

        def format_time(time):
            minutes, seconds = divmod(time, 60)
            hours, minutes = divmod(minutes, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        async def update_timer():
            nonlocal start_time, running, paused, desired_time
            while running and not paused:
                elapsed_time = int(time.time() - start_time)
                time_text.value = format_time(elapsed_time)
                page.update()
                if elapsed_time >= desired_time:
                    running = False
                    paused = False

                    winsound.Beep(2500, 1000)  # Emitir um som de beep
                await asyncio.sleep(1)

        async def start_timer(e):
            nonlocal start_time, running, paused, desired_time
            if not running:
            # Mudar cor do botão "Iniciar" para azul
                start_button.bgcolor = "#007BFF"
                start_button.update()
            
                desired_time = desired_time_input.value
                start_time = time.time()
                running = True
                paused = False
                page.update()
                await update_timer()

            # Voltar cor do botão "Iniciar" para verde ao terminar
                start_button.bgcolor = "#05A805"
                start_button.update()

        async def pause_timer(e):
            nonlocal paused
            paused = not paused
            if paused:
            # Mudar cor do botão "Pausar" para amarelo
                pause_button.bgcolor = "#FFC107"
                pause_button.update()
            else:
            # Voltar cor do botão "Pausar" para verde
                pause_button.bgcolor = "#05A805"
                pause_button.update()
                await update_timer()  # Retomar o cronômetro
            page.update()

        async def reset_timer(e):
            nonlocal start_time, running, paused
            running = False
            paused = False
            start_time = 0
            time_text.value = "00:00:00"
            time_text.color = "white"
            page.update()

        # Mudar cor do botão "Zerar" para vermelho temporariamente
            reset_button.bgcolor = "#DC3545"
            reset_button.update()

            await asyncio.sleep(1)  # Tempo para mostrar a cor vermelha

        # Voltar cor do botão "Zerar" para verde
            reset_button.bgcolor = "#05A805"
            reset_button.update()

    #exercicio1
        img1 = ft.Container(ft.Image(src="http://www.ferrosports.com.br/img_external/pernas/image29.gif",width=450,height=300,fit=ft.ImageFit.CONTAIN,border_radius=20),width=450,height=300,offset=ft.Offset(x=0,y=-0.04),border_radius=20)
    #exercicio1
    
    #vezes
        vezes = ft.Container(ft.Image(src="vezes.png",width=450,height=300,fit=ft.ImageFit.CONTAIN),width=250,height=35,offset=ft.Offset(x=0.33,y=0))

    # Criar um botão para iniciar o cronômetro
        start_button = ft.ElevatedButton(text="Iniciar", on_click=start_timer, offset=ft.Offset(x=0.5, y=0), width=100, height=30, bgcolor="#05A805", color="white")

    # Criar um botão para pausar o cronômetro
        pause_button = ft.ElevatedButton(text="Pausar", on_click=pause_timer, offset=ft.Offset(x=0.5, y=0), width=100, height=30, bgcolor="#05A805", color="white")

    # Criar um botão para zerar o cronômetro
        reset_button = ft.ElevatedButton(text="Zerar", on_click=reset_timer, offset=ft.Offset(x=0.5, y=0), width=100, height=30, bgcolor="#05A805", color="white")
        def show_bottom_sheet():
            page.vertical_alignment = "center"
            page.horizontal_alignment = "center"
            
            bottom_sheet_content = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            ft.Image(src=gif, width=450, height=300, fit=ft.ImageFit.COVER, border_radius=20),
                            width=450, height=300, offset=ft.Offset(x=0, y=-0.04), border_radius=20
                        ),
                        ft.Text(value=exercise_name, size=30, color="white", weight="bold", text_align="center"),
                        ft.Column([time_text,desired_time_input,
                                       ft.Row([start_button,pause_button,reset_button])],alignment="center"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20,
                bgcolor="black",
                width=450,
                height=600
            )
            bottom_sheet = ft.CupertinoBottomSheet(content=bottom_sheet_content)
            page.show_bottom_sheet(bottom_sheet)

        show_bottom_sheet()

    def get_image_path(exercise):
        row = data[data['exercise'] == exercise].iloc[0]
        return row['image_path'] if pd.notna(row['image_path']) else "path/to/default_image.jpg"

    def show_exercises_page(part):
        exercises = plano.get(part, [])
        
        containers = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            ft.Image(src=get_image_path(exercise), fit=ft.ImageFit.COVER),
                            height=125, border_radius=0, width=180, offset=ft.Offset(x=-0.4, y=0), bgcolor="red",
                            shadow=ft.BoxShadow(spread_radius=1.8, blur_radius=50, offset=ft.Offset(0, 4), color="#03B403")
                        ),
                        ft.Text(value=exercise, size=20, color="white", weight="bold", text_align="center"),
                    ],
                    alignment="center"
                ),
                width=400,
                height=120,
                bgcolor="black",
                border_radius=20,
                shadow=ft.BoxShadow(spread_radius=2, blur_radius=12, offset=ft.Offset(4, 4), color="black"),
                on_click=lambda e, ex=exercise: show_exercise_details(page, ex)
            ) for exercise in exercises
        ]

        page.controls.clear()
        page.add(
            ft.Column(
                controls=[
                    ft.Row([
                        ft.IconButton(icon=ft.icons.ARROW_BACK, icon_size=40, on_click=on_generate_click, icon_color='white'),
                        ft.Text(f"Treino de {part.capitalize()}", size=30, weight=ft.FontWeight.BOLD, color="white")
                    ]),
                    ft.Container(
                        ft.Row([
                            ft.Text(value="3X - 12REP", color="white", weight="bold", size=30, text_align="center"),
                            ft.Image(src="alter imagem.png", width=100, height=100, fit=ft.ImageFit.CONTAIN)
                        ], alignment="center"),
                        width=400, height=120, bgcolor="black", border_radius=20,
                        shadow=ft.BoxShadow(spread_radius=2, blur_radius=12, offset=ft.Offset(4, 4), color="black")
                    ),
                    ft.Text(value=f"{len(exercises)} exercícios", color="white", weight="bold", size=25, text_align="right"),
                    *containers
                ]
            )
        )
        page.update()
        
    
    def on_generate_click(e):
        altura_value = altura.value
        peso_value = peso.value
        sexo_value = sexo.value.lower().strip()
        nivel_value = nivel.value.lower().strip()
        doenca_value = doenca.value.lower().strip()
        objetivo_value = objetivo.value.lower().strip()

        global plano
        plano = gerar_plano_treino(sexo_value, nivel_value, doenca_value,altura_value,peso_value,objetivo_value)
        restrição_value = restrição.value.lower().strip()
        preferencia_value = preferencia.value.lower().strip()
        vegano_value = vegano.value.lower().strip()
        doenca_alimentar_value = doenca_alimentar.value.lower().strip()
        
        global plano_nutri
        plano_nutri = gerar_plano_nutricao(restrição_value,preferencia_value,vegano_value,doenca_alimentar_value)
        
        page.controls.clear()

        def on_nav_change(e):
            selected_index = e.control.selected_index
            page.clean()  # Limpa o conteúdo da página

            if selected_index == 0:
                treino()
            elif selected_index == 1:
                alongamento()
            elif selected_index == 2:
                nutricao()
            elif selected_index == 3:
                plano_semanal_tela()

        page.scroll = ft.ScrollMode.ALWAYS
        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.icons.FITNESS_CENTER_OUTLINED, tooltip="Treinos", label="Treinos"),
                ft.NavigationDestination(icon=ft.icons.HEALTH_AND_SAFETY_OUTLINED, tooltip="Alongamento", label="Alongamento"),
                ft.NavigationDestination(icon=ft.icons.FOOD_BANK_SHARP, tooltip="Nutrição", label="Nutrição"),
                ft.NavigationDestination(icon=ft.icons.CALENDAR_MONTH, tooltip="Plano semanal", label="Plano semanal")
            ],
            on_change=on_nav_change,
            height=50,
            bgcolor=ft.colors.TRANSPARENT,
            indicator_color="#1FF454",
            elevation=False
        )

        def abrir(e):
            page.show_drawer(drawer)
        def modal(e):
            page.show_bottom_sheet(modal1)
        modal1 = ft.BottomSheet(content=ft.Container((ft.Container((ft.Text(value="Minhas informações",size=30,color="black",weight="bold",text_align="center")),
                                                                   width=450,height=60,border_radius=20,bgcolor="#03B403",on_click=suas_informaçoes)),width=450,height=200,border_radius=20,bgcolor="black"),bgcolor="black")

        treinos_texto = ft.Row([
            ft.IconButton(icon=ft.icons.MENU, icon_size=40, on_click=abrir, icon_color='white'),
            ft.Text(value="Treinos", color="white", weight="bold", size=45),
            ft.Container(ft.Image(src="nova_logo.png", fit=ft.ImageFit.CONTAIN, width=70, height=70, offset=ft.Offset(x=0.3, y=0)),on_click=modal)
        ], alignment=ft.MainAxisAlignment.CENTER)

        drawer = ft.NavigationDrawer(bgcolor="#03B403", controls=[
            ft.Container(height=12),
            ft.Text(value="Outros", size=30, weight="bold", text_align="center", color="white"),
            ft.Divider(thickness=2),
            ft.IconButton(icon=ft.icons.ARROW_BACK)
        ])

        cont_braço = ft.Stack([
            ft.Container(ft.Image(src="treino de braço.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Braço", color="white", size=40, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("braço")
            )
        ], width=400, height=120)

        cont_costas = ft.Stack([
            ft.Container(ft.Image(src="treino de costa.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Costa", color="white", size=40, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("costas")
            )
        ], width=400, height=120)

        cont_abdomen = ft.Stack([
            ft.Container(ft.Image(src="treino de abdomen.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Abdômen", color="white", size=35, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("abdômen")
            )
        ], width=400, height=120)

        cont_perna = ft.Stack([
            ft.Container(ft.Image(src="treino de perna.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Perna", color="white", size=40, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("perna")
            )
        ], width=400, height=120)

        cont_peito = ft.Stack([
            ft.Container(ft.Image(src="treino de peito.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Peito", color="white", size=40, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("peito")
            )
        ], width=400, height=120)

        cont_ombros = ft.Stack([
            ft.Container(ft.Image(src="treino de ombros.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Ombro", color="white", size=40, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("ombro")
            )
        ], width=400, height=120)
        cont_gluteo = ft.Stack([ft.Container(ft.Image(src="treino de gluteo.jpg",width=400,height=120,fit=ft.ImageFit.COVER),width=400,height=120,border_radius=20),
                               
                               ft.Container(content=ft.Column([ft.Text("Treino de Gluteo",color="white",size=40,weight="bold")],  
                                                                                         
                   alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=5),  
                                                      
                   alignment=ft.alignment.center,width=400,height=120, on_click=lambda e: show_exercises_page("glúteo"))
        ],width=400,height=120)

        page.add(
            ft.Column(
                controls=[
                    treinos_texto,
                    cont_braço,
                    cont_costas,
                    cont_abdomen,
                    cont_perna,
                    cont_peito,
                    cont_ombros,
                    cont_gluteo
                ]
            )
        )
        page.update()

    def treino():
        page.controls.clear()
        def abrir(e):
            page.show_drawer(drawer)
        def modal(e):
            page.show_bottom_sheet(modal1)
        modal1 = ft.BottomSheet(content=ft.Container((ft.Container((ft.Text(value="Minhas informações",size=30,color="black",weight="bold",text_align="center")),
                                                                   width=450,height=60,border_radius=20,bgcolor="#03B403",on_click=suas_informaçoes)),width=450,height=200,border_radius=20,bgcolor="black"),bgcolor="black")

        treinos_texto = ft.Row([
            ft.IconButton(icon=ft.icons.MENU, icon_size=40, on_click=abrir, icon_color='white'),
            ft.Text(value="Treinos", color="white", weight="bold", size=45),
            ft.Container(ft.Image(src="nova_logo.png", fit=ft.ImageFit.CONTAIN, width=70, height=70, offset=ft.Offset(x=0.3, y=0)),on_click=modal)
        ], alignment=ft.MainAxisAlignment.CENTER)

        drawer = ft.NavigationDrawer(bgcolor="#03B403", controls=[
            ft.Container(height=12),
            ft.Text(value="Outros", size=30, weight="bold", text_align="center", color="white"),
            ft.Divider(thickness=2),
            ft.IconButton(icon=ft.icons.ARROW_BACK,on_click=suas_informaçoes)
        ])

        cont_braço = ft.Stack([
            ft.Container(ft.Image(src="treino de braço.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Braço", color="white", size=40, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("braço")
            )
        ], width=400, height=120)

        cont_costas = ft.Stack([
            ft.Container(ft.Image(src="treino de costa.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Costa", color="white", size=40, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("costas")
            )
        ], width=400, height=120)

        cont_abdomen = ft.Stack([
            ft.Container(ft.Image(src="treino de abdomen.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Abdômen", color="white", size=35, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("abdômen")
            )
        ], width=400, height=120)

        cont_perna = ft.Stack([
            ft.Container(ft.Image(src="treino de perna.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Perna", color="white", size=40, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("perna")
            )
        ], width=400, height=120)

        cont_peito = ft.Stack([
            ft.Container(ft.Image(src="treino de peito.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Peito", color="white", size=40, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("peito")
            )
        ], width=400, height=120)

        cont_ombros = ft.Stack([
            ft.Container(ft.Image(src="treino de ombros.png", width=400, height=120, fit=ft.ImageFit.COVER), width=400, height=120, border_radius=20),
            ft.Container(
                content=ft.Column([ft.Text("Treino de Ombro", color="white", size=40, weight="bold")],
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center, width=400, height=120, on_click=lambda e: show_exercises_page("ombro")
            )
        ], width=400, height=120)
        cont_gluteo = ft.Stack([ft.Container(ft.Image(src="treino de gluteo.jpg",width=400,height=120,fit=ft.ImageFit.COVER),width=400,height=120,border_radius=20),
                               
                               ft.Container(content=ft.Column([ft.Text("Treino de Gluteo",color="white",size=40,weight="bold")],  
                                                                                         
                   alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=5),  
                                                      
                   alignment=ft.alignment.center,width=400,height=120, on_click=lambda e: show_exercises_page("glúteo"))
        ],width=400,height=120)
        page.add(
            ft.Column(
                controls=[
                    treinos_texto,
                    cont_braço,
                    cont_costas,
                    cont_abdomen,
                    cont_perna,
                    cont_peito,
                    cont_ombros,
                    cont_gluteo
                ]
            )
        )
        page.update()
        page.update()

    def alongamento():
        page.controls.clear()
        page.add(ft.Column([
            ft.Text("Alongamento", size=30, weight="bold", color="white"),
            # Adicione mais conteúdo para a tela de alongamento se necessário
        ]))
        page.update()
        
    
        
    def get_image_path_food(etapa):
        row = data_nutri[data_nutri['etapas'] == etapa].iloc[0]
        return row['imagem_alimento'] if pd.notna(row['imagem_alimento']) else "path/to/default_image.jpg"
    
    def show_exercise_details_food(page, alimento_name):
        row = data_nutri[data_nutri["etapas"] == alimento_name].iloc[0]
        gif_ali = row['imagem_alimento']
        text_ali = row['alimentos']
        carboidratos = row['carboidratos']
        proteinas = row['proteinas']
        gordura = row['gordura']
        vitamina = row['vitamina']
        açucar = row['acuçar']
        receita = row['video']
        
    
        # def show_bottom_sheet_nutri():
        #     page.vertical_alignment = "center"
        #     page.horizontal_alignment = "center"
        #     page.scroll = ft.ScrollMode.ALWAYS
        
        #     bottom_sheet_content = ft.Container(
        #     content=ft.Column(
        #         controls=[
        #             ft.Container(
        #                 ft.Image(src=gif_ali, width=450, height=300, fit=ft.ImageFit.COVER, border_radius=20),
        #                 width=450, height=300, offset=ft.Offset(x=0, y=-0.04), border_radius=20
        #             ),
        #             ft.Text(value=alimento_name, size=30, color="white", weight="bold", text_align="center"),
                  
                    
                   
        #         ],
        #         alignment=ft.MainAxisAlignment.CENTER,
        #         horizontal_alignment=ft.CrossAxisAlignment.CENTER
        #     ),
        #     padding=20,
        #     bgcolor="black",
        #     width=450,
        #     height=600
        #     )
        #     bottom_sheet = ft.CupertinoBottomSheet(content=bottom_sheet_content)
        #     page.show_bottom_sheet(bottom_sheet)

        # show_bottom_sheet_nutri()
        def video_receita(e):
            sample_media = [
            ft.VideoMedia(
                        receita,
                    ),
                ]

            video = ft.Video(
            playlist=sample_media,
            playlist_mode=ft.PlaylistMode.LOOP,
            fill_color=ft.colors.BLACK,
            aspect_ratio=30/20,
            volume=100,
            autoplay=True,
            filter_quality=ft.FilterQuality.HIGH,
            muted=False,
            width=450,
            height=300,
            expand=True
        )

            alimento_video = ft.Container(
            content=ft.Column(
            controls=[
                video
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
            padding=20,
            bgcolor="black",
            width=450,
            height=600
    )

            bottom_sheet = ft.BottomSheet(content=alimento_video)

            page.show_bottom_sheet(bottom_sheet)
            page.update()
            
            
            
        def show_bottom_sheet_nutri():
            page.vertical_alignment = "center"
            page.horizontal_alignment = "center"
            page.scroll = ft.ScrollMode.ALWAYS
            page.clean()
            bnt_voltar = ft.IconButton(icon=ft.icons.ARROW_BACK, icon_size=40, on_click=nutricao, icon_color='white')
            img_alimento = ft.Column([ft.Container((ft.Image(src=gif_ali, width=300, height=300, fit=ft.ImageFit.COVER, border_radius=20)),
                                                   )])
            nome = ft.Text(value=text_ali,size=40,weight="bold",color="white")
            
            informações_ali = ft.Container((ft.Row([ft.Column([ft.Text(value="Informações nutricionais:",size=30,weight="bold",color="white"),
                                                               ft.Text(value=f"Carboidratos: {carboidratos}",size=24,color="blue",weight="bold"),
                                                               ft.Text(value=f"Proteinas: {proteinas}",size=24,color="yellow",weight="bold"),
                                                               ft.Text(value=f"Gordura: {gordura}",size=24,color="purple",weight="bold"),
                                                               ft.Text(value=f"Vitamina: {vitamina}",size=24,color="red",weight="bold"),
                                                               ft.Text(value=f"Açucar: {açucar}",size=24,color="orange",weight="bold")])],alignment="left")),width=400,height=280,bgcolor="#01e425",border_radius=20,padding=10)
                                                               
                                                               
            
            incredientes_ali = ft.Container((ft.Row([ft.Column([ft.Text(value="Ingredientes:",size=30,weight="bold",color="white")])],alignment="left")),width=400,height=280,bgcolor="#01e425",border_radius=20,padding=10)
            normal_radius = 120
            hover_radius = 120
            normal_title_style = ft.TextStyle(
                size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
            )
            hover_title_style = ft.TextStyle(
                size=16,
                color=ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
            )
            normal_badge_size = 40
            hover_badge_size = 50
    

            def badge(icon, size):
                return ft.Container(
                    ft.Icon(icon),
                    width=size,
                    height=size,
                    border=ft.border.all(1, ft.colors.BROWN),
                    border_radius=size / 2,
                    bgcolor=ft.colors.WHITE,
                )

            def on_chart_event(e: ft.PieChartEvent):
                for idx, section in enumerate(chart.sections):
                    if idx == e.section_index:
                        section.radius = hover_radius
                        section.title_style = hover_title_style
                    else:
                        section.radius = normal_radius
                        section.title_style = normal_title_style
                chart.update()

            chart = ft.PieChart(
                sections=[
                    ft.PieChartSection(
                        carboidratos,
                        title=f"{carboidratos}%",
                        title_style=normal_title_style,
                        color=ft.colors.BLUE,
                        radius=normal_radius,
                        badge=badge(ft.icons.AC_UNIT, normal_badge_size),
                        badge_position=0.98,
                    ),
                    ft.PieChartSection(
                        proteinas,
                        title=f"{proteinas}%",
                        title_style=normal_title_style,
                        color=ft.colors.YELLOW,
                        radius=normal_radius,
                        badge=badge(ft.icons.ACCESS_ALARM, normal_badge_size),
                        badge_position=0.98,
                    ),
                    ft.PieChartSection(
                        gordura,
                        title=f"{gordura}%",
                        title_style=normal_title_style,
                        color=ft.colors.PURPLE,
                        radius=normal_radius,
                        badge=badge(ft.icons.APPLE, normal_badge_size),
                        badge_position=0.98,
                    ),
                    ft.PieChartSection(
                        vitamina,
                        title=f"{vitamina}",
                        title_style=normal_title_style,
                        color=ft.colors.RED,
                        radius=normal_radius,
                        badge=badge(ft.icons.PEDAL_BIKE, normal_badge_size),
                        badge_position=0.98,
                    ),
                    ft.PieChartSection(
                        açucar,
                        title=f"{açucar}",
                        title_style=normal_title_style,
                        color=ft.colors.ORANGE,
                        radius=normal_radius,
                        badge=badge(ft.icons.FOOD_BANK_SHARP, normal_badge_size),
                        badge_position=0.98,
                    ),
                ],
                sections_space=0,
                center_space_radius=0,
                on_chart_event=on_chart_event,
                expand=False,
            )


            
            
            video = ft.Container((ft.Row([ft.Text(value="Ver vídeo",size=30,weight="bold",color="white")],alignment="center")),width=400,height=80,bgcolor="#01e425",border_radius=20,padding=10,on_click=video_receita)
            # nome = ft.Image(src=text_ali, width=50, height=30, fit=ft.ImageFit.COVER)
            page.bgcolor="#03B403"
            page.add(bnt_voltar,img_alimento,nome,informações_ali,incredientes_ali,chart,video)
            page.update()
        
            
        show_bottom_sheet_nutri()
        
    def show_food_page(dia):
        etapas = plano_nutri.get(dia, [])
        
        containers = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row([ft.Container(
                            ft.Image(src=get_image_path_food(etapa), fit=ft.ImageFit.COVER),
                            height=180, border_radius=0, width=200,
                            shadow=ft.BoxShadow(spread_radius=1.8, blur_radius=50, offset=ft.Offset(0, 4), color=ft.colors.TRANSPARENT)
                    )],alignment="center"),
                        ft.Row([ft.Text(value=etapa, size=30, color="white", weight="bold")],alignment="center"),
                    ],
                    alignment="center"
                ),
                width=250,
                height=250,
                bgcolor="#01e425",
                border_radius=20,
                shadow=ft.BoxShadow(spread_radius=2, blur_radius=12, offset=ft.Offset(4, 4), color="black"),
                on_click=lambda e, ex_ali=etapa:show_exercise_details_food(page, ex_ali)
            ) for etapa in etapas
        ]
       
        page.controls.clear()
        page.add(
            ft.Column(
                controls=[
                    ft.Row([
                        ft.IconButton(icon=ft.icons.ARROW_BACK, icon_size=40, on_click=nutricao, icon_color='white'),
                        ft.Text(f"{dia.capitalize()}", size=30, weight=ft.FontWeight.BOLD, color="white")
                    ]),
                    
                    ft.Text(value=f"{len(etapas)} alimentos", color="white", weight="bold", size=25, text_align="right"),
                    *containers
                ]
            )
        )
        page.update()
    #nutrição
    # def get_image_path_food(alimento):
    #     row = data_nutri[data_nutri['etapas'] == alimento].iloc[12]
    #     return row['imagem_alimento'] if pd.notna(row['imagem_alimento']) else "path/to/default_image.jpg"

    # def show_food_page(dia):
    #     global plano_nutri
    
    #     alimentos = plano_nutri.get(dia, [])
    
    #     containers = [
    #     ft.Container(
    #         content=ft.Row(
    #             controls=[
    #                 ft.Container(
    #                     ft.Image(src="", fit=ft.ImageFit.COVER),
    #                     height=125, width=180, border_radius=0, offset=ft.Offset(x=-0.4, y=0),
    #                     bgcolor="red", shadow=ft.BoxShadow(spread_radius=1.8, blur_radius=50, offset=ft.Offset(0, 4), color="#03B403")
    #                 ),
    #                 ft.Text(value=alimento, size=20, color="white", weight="bold", text_align="center"),
    #             ],
    #             alignment="center"
    #         ),
    #             width=400,
    #             height=120,
    #             bgcolor="black",
    #             border_radius=20,
    #             shadow=ft.BoxShadow(spread_radius=2, blur_radius=12, offset=ft.Offset(4, 4), color="black"),
    #             on_click=nutricao
    #         ) for alimento in alimentos
    #     ]

    #     page.controls.clear()
    #     page.add(
    #     ft.Column(
    #         controls=[
    #             ft.Row([
    #                 ft.IconButton(icon=ft.icons.ARROW_BACK, icon_size=40, on_click=on_generate_click, icon_color='white'),
    #                 ft.Text(f"Plano de {dia.capitalize()}", size=30, weight=ft.FontWeight.BOLD, color="white")
    #             ]),
    #             ft.Container(
    #                 ft.Row([
    #                     ft.Text(value="3X - 12REP", color="white", weight="bold", size=30, text_align="center"),
    #                     ft.Image(src="alter imagem.png", width=100, height=100, fit=ft.ImageFit.CONTAIN)
    #                 ], alignment="center"),
    #                 width=400, height=120, bgcolor="black", border_radius=20,
    #                 shadow=ft.BoxShadow(spread_radius=2, blur_radius=12, offset=ft.Offset(4, 4), color="black")
    #                 ),
    #                 ft.Text(value=f"{len(alimentos)} alimentos", color="white", weight="bold", size=25, text_align="right"),
    #                 *containers
    #             ]
    #         )
    #     )
    #     page.update()
    
    def nutricao():
        page.controls.clear()
    
    
        page.scroll = ft.ScrollMode.ALWAYS
        valor1 = float(altura.value)
        valor2 = float(peso.value)
            
            # Calcula a soma
        soma = valor2 / (valor1 ** 2)
        nome = ft.Column([
            ft.Text("Nutrição", size=45, weight="bold", color="white"),
            # Adicione mais conteúdo para a tela de nutrição se necessário
        ])
        # def imc(soma):
        #     if soma < 18.5:
        #         color = "red"  # Abaixo do peso
        #     elif 18.5 <= soma <= 24.9:
        #         color = "green"  # Peso normal
        #     elif 25 <= soma <= 29.9:
        #         color = "orange"  # Sobrepeso
        #     else:  # soma >= 30
        #         color = "red"  # Obesidade
    
        #     return color
        imc_info = ft.Column([ft.Container((ft.Row([ft.Column([ft.Text(value="IMC",size=26,color="white",weight="bold"),ft.Text(value=f"{soma:.1f}",size=25,color="#01e425",weight="bold")]),
                                                    ft.Image(src="maça_nutrição.png",width=162,height=159.3,fit=ft.ImageFit.CONTAIN),
                                                    ft.Image(src="info_imc.png",width=108.9,height=159.3,fit=ft.ImageFit.CONTAIN)],alignment="center")),width=420,height=170,border_radius=20,bgcolor="black"),
                              ft.Text(value="Dias da semana:",size=35,color="white",weight="bold")])
        segunda = ft.Row([ft.Container((ft.Row([ft.Text(value="Segunda",size=30,color="white",weight="bold",text_align="center")],alignment="center")),
                                       width=301.2,height=82.6,border_radius=20,bgcolor="#01e425", on_click=lambda e: show_food_page("segunda"))],alignment="left")
        
        terça = ft.Row([ft.Container((ft.Row([ft.Text(value="Terça",size=30,color="white",weight="bold",text_align="center")],alignment="center")),
                                       width=301.2,height=82.6,border_radius=20,bgcolor="#01e425", on_click=lambda e: show_food_page("terça"))],alignment="left")
        
        quarta = ft.Row([ft.Container((ft.Row([ft.Text(value="Quarta",size=30,color="white",weight="bold",text_align="center")],alignment="center")),
                                       width=301.2,height=82.6,border_radius=20,bgcolor="#01e425", on_click=lambda e: show_food_page("quarta"))],alignment="left")
        
        quinta = ft.Row([ft.Container((ft.Row([ft.Text(value="Quinta",size=30,color="white",weight="bold",text_align="center")],alignment="center")),
                                       width=301.2,height=82.6,border_radius=20,bgcolor="#01e425", on_click=lambda e: show_food_page("quinta"))],alignment="left")
        
        sexta = ft.Row([ft.Container((ft.Row([ft.Text(value="Sexta",size=30,color="white",weight="bold",text_align="center")],alignment="center")),
                                       width=301.2,height=82.6,border_radius=20,bgcolor="#01e425", on_click=lambda e: show_food_page("sexta"))],alignment="left")
        
        sabado = ft.Row([ft.Container((ft.Row([ft.Text(value="Sábado",size=30,color="white",weight="bold",text_align="center")],alignment="center")),
                                       width=301.2,height=82.6,border_radius=20,bgcolor="#01e425", on_click=lambda e: show_food_page("sabado"))],alignment="left")
        
        domingo = ft.Row([ft.Container((ft.Row([ft.Text(value="Domingo",size=30,color="white",weight="bold",text_align="center")],alignment="center")),
                                       width=301.2,height=82.6,border_radius=20,bgcolor="#01e425", on_click=lambda e: show_food_page("domingo"))],alignment="left")
        page.add(nome,imc_info,segunda,terça,quarta,quinta,sexta,sabado,domingo)
        page.update()
        # nome = ft.Column([
        #     ft.Text("Nutrição", size=45, weight="bold", color="white"),
        #     # Adicione mais conteúdo para a tela de nutrição se necessário
        # ])
        # imc_info = ft.Column([ft.Container((ft.Row([ft.Column([ft.Text(value="IMC:",size=26,color="white",weight="bold"),ft.Text(value="24",size=25,color="#01e425",weight="bold")]),
        #                                             ft.Image(src="maça_nutrição.png",width=162,height=159.3,fit=ft.ImageFit.CONTAIN),
        #                                             ft.Image(src="info_imc.png",width=108.9,height=159.3,fit=ft.ImageFit.CONTAIN)],alignment="center")),width=420,height=170,border_radius=20,bgcolor="black"),
        #                       ft.Text(value="Dias da semana:",size=35,color="white",weight="bold")])
        # def segunda_ali(e):
        #     page.clean()
        #     voltars = ft.Row([ft.IconButton(icon=ft.icons.ARROW_BACK, icon_size=40, on_click=nutricao, icon_color='white')],alignment="left")
        #     dias = ft.Row([ft.Text(value="Segunda",size=45,color="white",weight="bold")],alignment="letf")

        #     contalimentose = ft.Column([ft.Row([ft.Container((ft.Column([ft.Image(src="",width=90,height=90,fit=ft.ImageFit.CONTAIN),ft.Text(value="ola",size=30,color="white",text_align="center")])),width=200,height=208.7,border_radius=20,bgcolor="#01e425"),
        #                                        ft.Container((ft.Column([ft.Image(src="",width=90,height=90,fit=ft.ImageFit.CONTAIN),ft.Text(value="ola",size=30,color="white",text_align="center")])),width=200,height=208.7,border_radius=20,bgcolor="#01e425")]),

        #                                        ft.Row([ft.Container((ft.Column([ft.Image(src="",width=90,height=90,fit=ft.ImageFit.CONTAIN),ft.Text(value="ola",size=30,color="white",text_align="center")])),width=200,height=208.7,border_radius=20,bgcolor="#01e425"),
        #                                        ft.Container((ft.Column([ft.Image(src="",width=90,height=90,fit=ft.ImageFit.CONTAIN),ft.Text(value="ola",size=30,color="white",text_align="center")])),width=200,height=208.7,border_radius=20,bgcolor="#01e425")]),

        #                                        ft.Row([ft.Container((ft.Column([ft.Image(src="",width=90,height=90,fit=ft.ImageFit.CONTAIN),ft.Text(value="ola",size=30,color="white",text_align="center")])),width=200,height=208.7,border_radius=20,bgcolor="#01e425"),
        #                                        ft.Container((ft.Column([ft.Image(src="",width=90,height=90,fit=ft.ImageFit.CONTAIN),ft.Text(value="ola",size=30,color="white",text_align="center")])),width=200,height=208.7,border_radius=20,bgcolor="#01e425")]),

        #                                        ])
        #     page.add(voltars,dias,contalimentose)
        #     page.update()
        

        nome = ft.Column([
            ft.Text("Nutrição", size=45, weight="bold", color="white"),
            # Adicione mais conteúdo para a tela de nutrição se necessário
        ])
        

    def plano_semanal_tela():
            page.clean()
            page.bgcolor = "#03B403"
            page.vertical_alignment = "center"
            page.horizontal_alignment = "center"
            page.window_width = 450
            page.window_height = 700
   
            def handle_change(e: ft.ControlEvent):
                print(f"change on panel with index {e.data}")

            panel = ft.ExpansionPanelList(
                expand_icon_color="#1FF454",
                elevation=8,
                divider_color="#1FF454",
                on_change=handle_change)
            

            dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

            for i in range(7):
                exp = ft.ExpansionPanel(
                    header=ft.ListTile(title=ft.Text(dias_semana[i], size=30, weight="bold")))

                text = ft.Text("Seu treino do dia", size=24, text_align="center", weight="bold", color="white")
                text_field = ft.TextField(value="", width=400, visible=False, color="white", text_align="center")
                icon_button = ft.IconButton(ft.icons.EDIT, icon_color="blue")
                save_button = ft.ElevatedButton(f"Salvar", disabled=False, color="black", bgcolor="white")

                def create_callbacks(text, text_field, icon_button, save_button):
                    def on_edit_icon_click(e):
                        text.visible = False
                        text_field.visible = True
                        icon_button.disabled = True
                        save_button.disabled = False
                        page.update()

                    def on_save_button_click(e):
                        text.value = text_field.value
                        text.visible = True
                        text_field.visible = False
                        icon_button.disabled = False
                        save_button.disabled = True
                        page.update()

                    return on_edit_icon_click, on_save_button_click

                on_edit_icon_click, on_save_button_click = create_callbacks(text, text_field, icon_button, save_button)

                icon_button.on_click = on_edit_icon_click
                save_button.on_click = on_save_button_click
                

                container = ft.Container(width=300, height=40, bgcolor="black", border_radius=20, border=None,
                                 content=ft.Column(controls=[text, text_field],
                                                   horizontal_alignment=ft.CrossAxisAlignment.CENTER))

                linha = ft.Row(controls=[container,
                                 ft.Column(controls=[icon_button, save_button],
                                           alignment=ft.MainAxisAlignment.END)])

        # Wrap the content in a red Container
                red_container = ft.Container(bgcolor="#1FF454", content=linha)

                exp.content = red_container
                panel.controls.append(exp)
            titulo = ft.Text(value="Sua preferencia de treino:",size=30,color="white",weight="bold")

            page.add(titulo,panel)
            page.update()
            
    def alimentacao(e):
        page.clean()
        page.clean()
        voltar = ft.Row([ft.IconButton(icon=ft.icons.ARROW_BACK, icon_size=40, on_click=suas_informaçoes, icon_color='white')],alignment="left")
       
        
        st = ft.Stack([ft.Container(ft.Image(src="alimentol.webp",width=600,height=500,
                                         
                   fit=ft.ImageFit.COVER),width=600,height=500,border_radius=20),
                   
                   
                   ft.Container(content=ft.Column([ft.Text("Alimentação",color="white",size=45,weight="bold"),
                                                   
                  restrição,
                  preferencia,
                  vegano,
                  doenca_alimentar,

                   ft.ElevatedButton(text="Proximo",width=300,height=50,bgcolor="blue",color="white",on_click=on_generate_click)],
                                                  
                   alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=5),
                                
                   alignment=ft.alignment.center,width=600,height=500)],width=600,height=500)
         
        page.add(voltar,st)
        page.update()
        page.update()
    
    # Função para exibir a tela de suas informações
    def suas_informaçoes(e):
        page.clean()
        
        # Crie os campos de entrada aqui
       
        
        # Campos de sexo e nível
       
    
        st = ft.Stack([
            ft.Container(ft.Image(src="consulta-médica.jpg", width=600, height=500, fit=ft.ImageFit.COVER), width=600, height=500, border_radius=20),
            ft.Container(content=ft.Column([
                ft.Text("Suas Informações", color="white", size=45, weight="bold"),
                altura,
                peso,
                sexo,
                nivel,
                doenca,
                objetivo,
                ft.ElevatedButton(text="Salvar", width=300, height=50, bgcolor="blue", color="white", on_click=alimentacao)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center, width=600, height=500)
        ], width=600, height=500)
        
        page.add(st)
        page.update()
    
    # Função para a tela de login
    def fazer_login(e):
        page.clean()
        email = ft.TextField(label="Email", width=300, height=50, bgcolor="white", border_radius=10)
        senha = ft.TextField(label="Senha", width=300, height=50, bgcolor="white", password=True, can_reveal_password=True, border_radius=10)
        
        st = ft.Stack([
            ft.Container(ft.Image(src="fazer login.jpg", width=600, height=500, fit=ft.ImageFit.COVER), width=600, height=500, border_radius=20),
            ft.Container(content=ft.Column([
                ft.Text("Fazer login", color="white", size=45, weight="bold"),
                email,
                senha,
                ft.ElevatedButton(text="Entrar", width=300, height=50, bgcolor="blue", color="white", on_click=suas_informaçoes)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20), alignment=ft.alignment.center, width=600, height=500)
        ], width=600, height=500)
        
        page.add(st)
        page.update()
    
    # Função para cadastro
    def cadastro(e):
        page.clean()
        usuario = ft.TextField(label="Nome", width=300, height=50, bgcolor="white", border_radius=10)
        email = ft.TextField(label="Email", width=300, height=50, bgcolor="white", border_radius=10) 
        senha = ft.TextField(label="Senha", width=300, height=50, bgcolor="white", password=True, can_reveal_password=True, border_radius=10)
        ja_possui = ft.Row([
            ft.Text(value="Já possui uma conta?", size=20, color="white", weight="bold"),
            ft.Container(ft.Text(value="Fazer login", size=20, color="blue", weight="bold"), on_click=fazer_login)
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        st = ft.Stack([
            ft.Container(ft.Image(src="teste copy.jpg", width=600, height=500, fit=ft.ImageFit.COVER), width=600, height=500, border_radius=20),
            ft.Container(content=ft.Column([
                ft.Text("Cadastro", color="white", size=45, weight="bold"),                              
                usuario,
                email,
                senha,
                ja_possui, 
                ft.ElevatedButton(text="Entrar", width=300, height=50, bgcolor="blue", color="white", on_click=suas_informaçoes)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20), alignment=ft.alignment.center, width=600, height=500)
        ], width=600, height=500)
        
        page.add(st)
        page.update()
    
    # Animação   
    def animacao(e):
        if e.data == "true":
            container.width = 400
            container.height = 400
            container.background_color = ft.colors.YELLOW
        else:
            container.width = 300
            container.height = 300
            container.background_color = ft.colors.TRANSPARENT
        page.update()
    container = ft.Container(content=ft.Image(src="nova_logo.png", fit=ft.ImageFit.CONTAIN), width=400, height=400,
                             bgcolor=ft.colors.TRANSPARENT, animate=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE),
                             on_hover=animacao, on_click=cadastro)
    page.add(container)
    page.update()

ft.app(target=main) 
