import flet as ft
from utils.ui import show_message
from apis.receitaws import cnpj_lookup
from apis.customer_vendor import create_new_customer_vendor

class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.codcoligada = str()
        self.customers_vendors = dict()
        
        self.cnpj_ref = ft.Ref[ft.TextField]()
        self.ie_ref = ft.Ref[ft.TextField]()
        self.type_ref = ft.Ref[ft.Dropdown]()
        self.list_view_ref = ft.Ref[ft.Column]()
        self.log_ref = ft.Ref[ft.Column]()

    def show(self):
        # Função para adicionar o item na lista e no dicionário
        def add_item(e):
            cnpj = self.cnpj_ref.current.value.strip()
            ie = self.ie_ref.current.value.strip()
            type_val = self.type_ref.current.value # "c" ou "f"

            if not cnpj or not type_val:
                self.page.snack_bar = ft.SnackBar(ft.Text("CNPJ e Tipo são obrigatórios!"))
                self.page.snack_bar.open = True
                self.page.update()
                return

            # Adiciona ao dicionário "customers_vendors"
            self.customers_vendors_data[cnpj] = [type_val, ie]

            # Adiciona visualmente na lista
            type_label = "Cliente" if type_val == "c" else "Fornecedor"
            self.list_view_ref.current.controls.append(
                ft.ListTile(
                    title=ft.Text(f"CNPJ: {cnpj}"),
                    subtitle=ft.Text(f"Tipo: {type_label} | IE: {ie if ie else 'Isento/Não informado'}"),
                    trailing=ft.IconButton(
                        ft.Icons.DELETE, 
                        on_click=lambda _, c=cnpj: remove_item(c) # Botão para remover
                    )
                )
            )
            
            # Limpa os campos
            self.cnpj_ref.current.value = ""
            self.ie_ref.current.value = ""
            self.cnpj_ref.current.focus()
            self.page.update()

        # Função para remover item
        def remove_item(cnpj_to_remove):
            if cnpj_to_remove in self.customers_vendors_data:
                del self.customers_vendors_data[cnpj_to_remove]
                
                # Reconstrói a lista visual (simples, mas eficaz para este caso)
                self.list_view_ref.current.controls.clear()
                for cnpj, data in self.customers_vendors_data.items():
                    t_val, ie_val = data
                    t_label = "Cliente" if t_val == "c" else "Fornecedor"
                    self.list_view_ref.current.controls.append(
                        ft.ListTile(
                            title=ft.Text(f"CNPJ: {cnpj}"),
                            subtitle=ft.Text(f"Tipo: {t_label} | IE: {ie_val}"),
                            trailing=ft.IconButton(ft.Icons.DELETE, on_click=lambda _, c=cnpj: remove_item(c))
                        )
                    )
                self.page.update()

        # Função principal de automação
        def start_automation(e):
            cod_coligada = self.codcoligada.current.value
            if not cod_coligada:
                show_message(self.page, "Erro", "Por favor, informe o ID da Coligada.")
                return

            if not self.customers_vendors_data:
                show_message(self.page, "Aviso", "A lista de cadastro está vazia.")
                return

            self.log_ref.current.controls.clear()
            self.log_ref.current.controls.append(ft.Text("Iniciando automação...", color="blue", weight="bold"))
            self.page.update()

            # Itera sobre o dicionário criado (igual ao customers_vendors.py)
            for cnpj, data in self.customers_vendors_data.items():
                cod_cfo = data[0] # "c" ou "f"
                inscricao_estadual = data[1]

                try:
                    self.log_ref.current.controls.append(ft.Text(f"Consultando CNPJ: {cnpj}..."))
                    self.page.update()

                    # 1. Consulta na ReceitaWS
                    # Note que a função cnpj_lookup espera (codcoligada, codcfo, cnpj, ie)
                    customer_data = cnpj_lookup(cod_coligada, cod_cfo, cnpj, inscricao_estadual)
                    
                    self.log_ref.current.controls.append(ft.Text(f"Dados obtidos: {customer_data['name']}"))
                    self.page.update()

                    # 2. Envia para a API do ERP
                    create_new_customer_vendor(
                        companyId=customer_data["companyId"],
                        code=customer_data["code"],
                        shortName=customer_data["shortName"],
                        name=customer_data["name"],
                        type=customer_data["type"],
                        mainNIF=customer_data["mainNIF"],
                        stateRegister=customer_data["stateRegister"],
                        zipCode=customer_data["zipCode"],
                        streetType=customer_data["streetType"],
                        streetName=customer_data["streetName"],
                        number=customer_data["number"],
                        districtType=customer_data["districtType"],
                        district=customer_data["district"],
                        stateCode=customer_data["stateCode"],
                        cityInternalId=customer_data["cityInternalId"],
                        phoneNumber=customer_data["phoneNumber"],
                        email=customer_data["email"],
                        contributor=customer_data["contributor"]
                    )

                    self.log_ref.current.controls.append(ft.Text(f"Sucesso: {cnpj} cadastrado!", color="green"))
                
                except Exception as ex:
                    self.log_ref.current.controls.append(ft.Text(f"Erro ao processar {cnpj}: {str(ex)}", color="red"))
                
                self.page.update()
            
            self.log_ref.current.controls.append(ft.Text("Processo finalizado.", weight="bold"))
            self.page.update()

        # Layout da Interface
        self.page.clean()
        
        # Campos de Input
        input_container = ft.Container(
            content=ft.Column([
                ft.Text("Configuração Inicial", size=20, weight="bold"),
                ft.TextField(ref=self.codcoligada, label="ID da Coligada (Ex: 1)", width=200),
                
                ft.Divider(),
                
                ft.Text("Adicionar Cliente/Fornecedor", size=18),
                ft.Row([
                    ft.TextField(ref=self.cnpj_ref, label="CNPJ", expand=True),
                    ft.TextField(ref=self.ie_ref, label="Inscrição Estadual (Opcional)", expand=True),
                    ft.Dropdown(
                        ref=self.type_ref, 
                        label="Tipo",
                        width=150,
                        options=[
                            ft.dropdown.Option("c", "Cliente"),
                            ft.dropdown.Option("f", "Fornecedor"),
                        ]
                    ),
                    ft.ElevatedButton("Adicionar", icon=ft.Icons.ADD, on_click=add_item)
                ])
            ]),
            padding=20,
            bgcolor=ft.Colors.GREY_100,
            border_radius=10
        )

        # Botão de Ação Principal
        action_button = ft.Button(
            "Iniciar Automação", 
            icon=ft.Icons.PLAY_ARROW, 
            style=ft.ButtonStyle(bgcolor="blue", color="white"),
            height=50,
            on_click=start_automation
        )

        # Área de Lista e Logs
        display_area = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Fila de Cadastro", weight="bold"),
                    ft.Column(ref=self.list_view_ref, scroll=ft.ScrollMode.AUTO, height=300)
                ]),
                expand=True,
                border=ft.border.all(1, "grey"),
                border_radius=5,
                padding=10
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Logs de Execução", weight="bold"),
                    ft.Column(ref=self.log_ref, scroll=ft.ScrollMode.AUTO, height=300)
                ]),
                expand=True,
                border=ft.border.all(1, "grey"),
                border_radius=5,
                padding=10
            )
        ], expand=True)

        self.page.add(
            ft.Column([
                input_container,
                ft.Container(content=action_button, alignment=ft.Alignment.CENTER, padding=10),
                display_area
            ], expand=True, spacing=20)
        )
        self.page.update()
