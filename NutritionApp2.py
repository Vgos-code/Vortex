"""
NutritionApp2.py

Um aplicativo de desktop desenvolvido com Tkinter para auxiliar nutricionistas
no cálculo das necessidades nutricionais de seus pacientes e na geração de
planos de refeições básicos.

Funcionalidades:
- Cálculo de Metabolismo Basal (BMR) usando a equação de Mifflin-St Jeor.
- Cálculo de calorias diárias recomendadas com base no nível de atividade.
- Cálculo do Índice de Massa Corporal (IMC) e sua classificação.
- Distribuição de macronutrientes (carboidratos, proteínas, gorduras).
- Recomendação de ingestão diária de água.
- Geração de um plano de refeições com opções para café da manhã, almoço,
  lanche da tarde e jantar, com número de opções configurável.
- Regeneração individual de categorias de refeições.
- Validação de entrada em tempo real para campos numéricos (Peso, Altura, Idade),
  com feedback visual (fundo rosa para entradas inválidas).
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random

# --- Funções de Cálculo Nutricional ---
# Estas funções são independentes da UI e realizam os cálculos nutricionais.

def calculate_bmr(weight, height, age, sex):
    """
    Calcula o Metabolismo Basal (BMR) usando a equação de Mifflin-St Jeor.
    Fórmula para homens: 10 * peso (kg) + 6.25 * altura (cm) - 5 * idade (anos) + 5
    Fórmula para mulheres: 10 * peso (kg) + 6.25 * altura (cm) - 5 * idade (anos) - 161
    """
    sex = sex.strip().lower()
    if sex not in ('m', 'f'):
        raise ValueError('Sexo deve ser "m" (masculino) ou "f" (feminino).')
    if sex == 'm':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else: # 'f'
        return 10 * weight + 6.25 * height - 5 * age - 161


def recommended_calories(bmr, activity_level):
    """
    Ajusta o BMR para calorias diárias recomendadas (TDEE) com base no nível de atividade.
    Multiplica o BMR por um fator correspondente ao nível de atividade.
    """
    levels = {
        'sedentário': 1.2,      # Pouco ou nenhum exercício
        'leve': 1.375,          # Exercício leve (1-3 dias/semana)
        'moderado': 1.55,       # Exercício moderado (3-5 dias/semana)
        'ativo': 1.725,         # Exercício pesado (6-7 dias/semana)
        'muito ativo': 1.9      # Exercício muito pesado (trabalho físico ou 2x dia)
    }
    key = activity_level.strip().lower()
    if key not in levels:
        raise ValueError('Nível de atividade inválido. Escolha entre: ' + ', '.join(levels.keys()))
    return bmr * levels[key]


def calculate_bmi(weight, height):
    """
    Calcula o Índice de Massa Corporal (IMC).
    Fórmula: peso (kg) / (altura (m))^2
    """
    if height <= 0:
        raise ValueError("Altura deve ser um valor positivo para calcular o IMC.")
    return weight / (height / 100) ** 2


def bmi_classification(bmi):
    """
    Retorna a classificação do IMC com base nos valores padrão.
    """
    if bmi < 18.5:
        return 'Abaixo do peso'
    elif bmi < 25: # 18.5 - 24.9
        return 'Peso normal'
    elif bmi < 30: # 25.0 - 29.9
        return 'Sobrepeso'
    else: # IMC >= 30
        return 'Obesidade'


def macro_distribution(calories):
    """
    Distribui as calorias totais em macronutrientes (carboidratos, proteínas, gorduras).
    Padrão: Carboidratos 50%, Proteínas 20%, Gorduras 30%.
    Converte as calorias de cada macro em gramas (1g carb/prot = 4 kcal, 1g gord = 9 kcal).
    """
    carbs_cal = calories * 0.50
    protein_cal = calories * 0.20
    fat_cal = calories * 0.30

    carbs_g = carbs_cal / 4
    protein_g = protein_cal / 4
    fat_g = fat_cal / 9
    return round(carbs_g), round(protein_g), round(fat_g)


def water_intake(weight):
    """
    Recomenda a ingestão diária de água em litros.
    Baseado na recomendação comum de 35 ml de água por kg de peso corporal.
    """
    return round(weight * 35 / 1000, 2)


# --- Classe Principal do Aplicativo ---

class NutritionApp(tk.Tk):
    """
    Classe principal para o aplicativo de nutrição.
    Gerencia a interface do usuário, entrada de dados, cálculos e exibição de resultados.
    """
    def __init__(self):
        super().__init__()
        self.title('Aplicativo de Apoio para Nutricionistas')
        self.geometry('800x800') # Tamanho inicial da janela
        self.resizable(True, True) # Permite redimensionamento

        # --- Configuração de Estilo ---
        # Define um estilo customizado para TEntry quando a validação falha.
        style = ttk.Style(self)
        style.configure("Error.TEntry", fieldbackground="pink")

        # --- Listas Mestras de Refeições ---
        # Estas listas contêm todas as opções de refeições disponíveis.
        self.all_breakfasts = [
            'Omelete de claras com espinafre e tomate', 'Iogurte grego com granola sem açúcar e frutas vermelhas',
            'Vitamina de banana com aveia e chia', 'Panqueca de aveia com mel e banana',
            'Tapioca com queijo cottage e peito de peru', 'Pão integral com abacate e ovo poché',
            'Mingau de aveia com maçã e canela', 'Smoothie verde com couve, abacaxi e gengibre',
            'Crepioca de frango desfiado', 'Waffle integral com iogurte e morango',
            'Sanduíche de pão integral com ricota e peito de peru', 'Parfait de iogurte, chia e kiwi',
            'Wrap de alface com ricota temperada', 'Overnight oats com leite de amêndoas e blueberries',
            'Pão sírio integral com homus e cenoura ralada', 'Muffin integral de banana e aveia',
            'Ovos mexidos com cogumelos e espinafre', 'Vitaminado de mamão e linhaça',
            'Crepioca de banana com canela', 'Smoothie bowl de frutas vermelhas e granola'
        ]
        self.all_lunches = [
            'Peito de frango grelhado, arroz integral e brócolis', 'Filé de peixe assado, purê de batata doce e salada verde',
            'Carne magra refogada com legumes e quinoa', 'Salada de atum com grão de bico e vinagrete de limão',
            'Frango ao curry com legumes no vapor', 'Tacos de alface com carne moída magra',
            'Espaguete de abobrinha ao pesto', 'Salada de lentilhas com cenoura e pepino',
            'Strogonoff de frango light com arroz integral', 'Quiche de espinafre light com salada de folhas',
            'Tilápia grelhada com legumes assados', 'Fricassê de grão de bico com espinafre',
            'Panqueca americana de aveia com recheio de frango', 'Berinjela recheada com carne magra e tomate',
            'Arroz de couve-flor com frango desfiado', 'Bife magro grelhado com mandioca cozida',
            'Feijão tropeiro light com couve e ovo cozido', 'Tabule de quinoa com ervas finas',
            'Wrap integral com peito de peru e salada', 'Sopa de legumes com carne magra desfiada'
        ]
        self.all_snacks = [
            'Banana com pasta de amendoim', 'Maçã fatiada com canela e nozes',
            'Iogurte natural com sementes de abóbora', 'Mix de castanhas e passas',
            'Barrinha de cereal integral caseira', 'Palitos de cenoura e pepino com homus',
            'Torrada integral com queijo branco', 'Vitamina de abacate com cacau',
            'Smoothie de morango e chia', 'Cookie integral de aveia e banana',
            'Pipoca de panela sem óleo', 'Pêssego com iogurte grego', 'Uvas congeladas',
            'Chips de batata doce assada', 'Bolinho de batata doce e aveia',
            'Tapioca simples com queijo de minas', 'Melancia em cubos', 'Vitamina de laranja e cenoura',
            'Geleia de fruta sem açúcar em torrada integral', 'Cereal integral com leite desnatado'
        ]
        self.all_dinners = [
            'Salmão grelhado com aspargos ao vapor', 'Tilápia ao forno com purê de mandioquinha',
            'Frango assado com abóbora e couve', 'Sopa cremosa de cenoura e gengibre',
            'Carne de panela magra com batata doce', 'Omelete de legumes variados',
            'Peito de peru grelhado com salada de rúcula', 'Berinjela à parmegiana light',
            'Salada de folhas verdes com ovo cozido', 'Quinoa com legumes e grão de bico',
            'Abobrinha recheada com cogumelos', 'Espaguete de pupunha ao molho de tomate',
            'Sardinha grelhada com salada de tomate', 'Quibe assado de forno com salada',
            'Camarão ao alho e óleo com legumes', 'Sopa de abóbora com sementes de girassol',
            'Carne moída magra refogada com vagem', 'Salmão ao vapor com brócolis',
            'Wrap de alface com frango grelhado', 'Panqueca integral de espinafre'
        ]

        # --- Variáveis de Tkinter para Entradas ---
        self.weight_var = tk.DoubleVar()
        self.height_var = tk.DoubleVar()
        self.age_var = tk.IntVar()
        self.sex_var = tk.StringVar(value='m') # Default para masculino
        self.activity_var = tk.StringVar(value='Sedentário') # Default
        self.num_meal_options_var = tk.IntVar(value=5) # Default para número de opções de refeição

        # --- Interface: Frame de Entrada de Dados do Paciente ---
        input_frame = ttk.LabelFrame(self, text='Dados do Paciente', padding=10)
        input_frame.pack(fill='x', padx=10, pady=10)

        # Layout em grid para os campos de entrada
        row = 0
        ttk.Label(input_frame, text='Peso (kg):').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.weight_entry = ttk.Entry(input_frame, textvariable=self.weight_var)
        self.weight_entry.grid(row=row, column=1, padx=5, pady=5)
        self.weight_entry.bind('<FocusOut>', lambda e, v=self.weight_var, w=self.weight_entry: self._validate_positive_numeric_input(e, v, w))
        self.weight_entry.bind('<KeyRelease>', lambda e, v=self.weight_var, w=self.weight_entry: self._validate_positive_numeric_input(e, v, w))
        row += 1

        ttk.Label(input_frame, text='Altura (cm):').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.height_entry = ttk.Entry(input_frame, textvariable=self.height_var)
        self.height_entry.grid(row=row, column=1, padx=5, pady=5)
        self.height_entry.bind('<FocusOut>', lambda e, v=self.height_var, w=self.height_entry: self._validate_positive_numeric_input(e, v, w))
        self.height_entry.bind('<KeyRelease>', lambda e, v=self.height_var, w=self.height_entry: self._validate_positive_numeric_input(e, v, w))
        row += 1

        ttk.Label(input_frame, text='Idade (anos):').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.age_entry = ttk.Entry(input_frame, textvariable=self.age_var)
        self.age_entry.grid(row=row, column=1, padx=5, pady=5)
        self.age_entry.bind('<FocusOut>', lambda e, v=self.age_var, w=self.age_entry: self._validate_positive_numeric_input(e, v, w))
        self.age_entry.bind('<KeyRelease>', lambda e, v=self.age_var, w=self.age_entry: self._validate_positive_numeric_input(e, v, w))
        row += 1

        ttk.Label(input_frame, text='Sexo:').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        sex_frame = ttk.Frame(input_frame) # Frame para agrupar Radiobuttons
        sex_frame.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        ttk.Radiobutton(sex_frame, text='Masculino', variable=self.sex_var, value='m').pack(side='left')
        ttk.Radiobutton(sex_frame, text='Feminino', variable=self.sex_var, value='f').pack(side='left')
        row += 1

        ttk.Label(input_frame, text='Nível de Atividade:').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        activity_options = ['Sedentário', 'Leve', 'Moderado', 'Ativo', 'Muito Ativo']
        activity_combo = ttk.Combobox(input_frame, values=activity_options, state='readonly', textvariable=self.activity_var)
        activity_combo.grid(row=row, column=1, padx=5, pady=5, sticky='ew') # sticky='ew' para expandir
        row += 1

        ttk.Label(input_frame, text='Número de opções de refeição:').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        ttk.Spinbox(input_frame, from_=1, to=20, textvariable=self.num_meal_options_var, width=5).grid(row=row, column=1, padx=5, pady=5, sticky='w')
        row += 1

        # --- Botão de Cálculo Principal ---
        ttk.Button(self, text='Calcular Plano Nutricional', command=self.calculate).pack(pady=10)

        # --- Interface: Frame de Exibição de Resultados ---
        self.results_frame = ttk.LabelFrame(self, text='Resultados Calculados', padding=10)
        self.results_frame.pack(fill='x', padx=10, pady=10)
        self.bmr_label = ttk.Label(self.results_frame, text='Metabolismo Basal (BMR): -')
        self.bmr_label.pack(anchor='w')
        self.cal_label = ttk.Label(self.results_frame, text='Calorias Recomendadas (TDEE): -')
        self.cal_label.pack(anchor='w')
        self.bmi_label = ttk.Label(self.results_frame, text='IMC: -')
        self.bmi_label.pack(anchor='w')
        self.class_label = ttk.Label(self.results_frame, text='Classificação IMC: -')
        self.class_label.pack(anchor='w')
        self.macro_label = ttk.Label(self.results_frame, text='Macros (g): Carboidratos -, Proteínas -, Gorduras -')
        self.macro_label.pack(anchor='w')
        self.water_label = ttk.Label(self.results_frame, text='Ingestão de água recomendada (L/dia): -')
        self.water_label.pack(anchor='w')

        # --- Interface: Notebook para Plano de Refeições ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        self.meal_texts = {} # Dicionário para armazenar os widgets Text de cada refeição
        meal_types = ['Café da Manhã', 'Almoço', 'Lanche da Tarde', 'Jantar']
        for meal_type in meal_types:
            frame = ttk.Frame(self.notebook) # Frame para cada aba do notebook
            self.notebook.add(frame, text=meal_type)

            # Sub-frame para organizar o Text e Scrollbar, permitindo que o botão fique abaixo
            text_area_frame = ttk.Frame(frame)
            text_area_frame.pack(side=tk.TOP, fill='both', expand=True)

            text_widget = tk.Text(text_area_frame, wrap='word', height=10) # `wrap='word'` para quebrar palavras longas
            text_widget.pack(side='left', fill='both', expand=True)

            scrollbar = ttk.Scrollbar(text_area_frame, orient='vertical', command=text_widget.yview)
            scrollbar.pack(side='right', fill='y')
            text_widget.configure(yscrollcommand=scrollbar.set)
            self.meal_texts[meal_type] = text_widget

            # Botão de regeneração para cada categoria de refeição
            # Usa lambda para passar o meal_type específico para o comando do botão
            regenerate_button = ttk.Button(frame, text=f"Regenerar {meal_type}",
                                           command=lambda mt=meal_type: self.regenerate_meal_category(mt))
            regenerate_button.pack(side=tk.BOTTOM, pady=5, fill='x')


    def calculate(self):
        """
        Método principal para calcular e exibir todas as informações nutricionais
        e o plano de refeições inicial.
        Chamado pelo botão "Calcular Plano Nutricional".
        """
        # 1. Validação Pré-Cálculo: Verifica se algum campo está marcado como erro.
        if any(w.cget("style") == "Error.TEntry" for w in [self.weight_entry, self.height_entry, self.age_entry]):
            messagebox.showerror("Entrada Inválida", "Corrija os campos destacados em rosa antes de calcular.")
            return

        try:
            # 2. Obtenção dos valores de entrada das variáveis Tkinter.
            #    A conversão para float/int é feita por .get(), que pode gerar tk.TclError.
            weight = self.weight_var.get()
            height = self.height_var.get()
            age = self.age_var.get()
            sex = self.sex_var.get()
            activity = self.activity_var.get()

            # 3. Validação Adicional dos Valores Obtidos:
            #    Garante que os valores numéricos são positivos.
            if weight <= 0 or height <= 0 or age <= 0:
                messagebox.showerror("Entrada Inválida", "Peso, Altura e Idade devem ser valores positivos.")
                if weight <=0: self.weight_entry.config(style="Error.TEntry")
                if height <=0: self.height_entry.config(style="Error.TEntry")
                if age <=0: self.age_entry.config(style="Error.TEntry")
                return

            # Obtenção e validação do número de opções de refeição.
            num_options_value = 5 # Default
            try:
                num_options_value = self.num_meal_options_var.get()
                if not (1 <= num_options_value <= 20): # Limite do Spinbox
                    messagebox.showwarning("Entrada Inválida", "Número de opções de refeição deve estar entre 1 e 20. Usando o padrão de 5.")
                    num_options_value = 5
                    self.num_meal_options_var.set(5)
            except tk.TclError:
                messagebox.showwarning("Entrada Inválida", "Número de opções de refeição inválido. Usando o padrão de 5.")
                num_options_value = 5
                self.num_meal_options_var.set(5)

            # 4. Execução dos Cálculos Nutricionais:
            bmr = calculate_bmr(weight, height, age, sex)
            calories = recommended_calories(bmr, activity)
            bmi = calculate_bmi(weight, height)
            classification = bmi_classification(bmi)
            carbs, prot, fat = macro_distribution(calories)
            water = water_intake(weight)

            # Geração do plano de refeições.
            plan = self._generate_meal_plan_data(num_options=num_options_value)

            # 5. Atualização da Interface com os Resultados:
            self.bmr_label.config(text=f'Metabolismo Basal (BMR): {bmr:.0f} kcal/dia')
            self.cal_label.config(text=f'Calorias Recomendadas (TDEE): {calories:.0f} kcal/dia')
            self.bmi_label.config(text=f'IMC: {bmi:.1f}')
            self.class_label.config(text=f'Classificação IMC: {classification}')
            self.macro_label.config(text=f'Macros (g): Carboidratos {carbs}, Proteínas {prot}, Gorduras {fat}')
            self.water_label.config(text=f'Ingestão de água recomendada (L/dia): {water}')

            # Preenchimento das abas do plano de refeições.
            for meal, text_widget in self.meal_texts.items():
                text_widget.delete('1.0', tk.END) # Limpa conteúdo anterior
                combos = plan.get(meal, [])
                for i, combo in enumerate(combos, 1):
                    text_widget.insert(tk.END, f'{i}. {combo}\n')

        except ValueError as ve: # Erros de valor nas funções de cálculo (e.g., sexo inválido)
            messagebox.showerror('Erro de Cálculo', f"Erro nos dados fornecidos: {str(ve)}")
        except tk.TclError as te: # Erros ao obter valores das variáveis Tkinter (e.g., entrada não numérica)
             messagebox.showerror('Erro de Entrada', f"Erro ao ler valor de entrada: {str(te)}. Verifique os campos Peso, Altura e Idade.")
        except Exception as e: # Captura geral para outros erros inesperados.
            messagebox.showerror('Erro Inesperado', f'Ocorreu um erro inesperado: {str(e)}')


    def regenerate_meal_category(self, meal_type):
        """
        Regenera as opções de refeição para uma categoria específica (meal_type).
        Chamado pelos botões "Regenerar" em cada aba de refeição.
        """
        try:
            num_options = self.num_meal_options_var.get()
            if not (1 <= num_options <= 20): # Valida o número de opções.
                messagebox.showwarning("Entrada Inválida", "Número de opções deve estar entre 1 e 20. Usando o padrão de 5.")
                num_options = 5
                self.num_meal_options_var.set(5)
        except tk.TclError: # Caso o valor no Spinbox seja inválido.
            messagebox.showwarning("Entrada Inválida", "Número de opções de refeição inválido. Usando o padrão de 5.")
            num_options = 5
            self.num_meal_options_var.set(5)

        new_meals = []
        source_list = [] # Lista de onde as refeições serão sorteadas.

        # Seleciona a lista mestre correta com base no meal_type.
        if meal_type == 'Café da Manhã': source_list = self.all_breakfasts
        elif meal_type == 'Almoço': source_list = self.all_lunches
        elif meal_type == 'Lanche da Tarde': source_list = self.all_snacks
        elif meal_type == 'Jantar': source_list = self.all_dinners

        if source_list:
            current_options = list(source_list) # Cria uma cópia para embaralhar.
            random.shuffle(current_options)
            new_meals = current_options[:num_options] # Seleciona o número desejado de opções.

        text_widget = self.meal_texts.get(meal_type) # Obtém o widget Text correspondente.
        if text_widget:
            text_widget.delete('1.0', tk.END) # Limpa opções antigas.
            for i, combo in enumerate(new_meals, 1): # Adiciona novas opções numeradas.
                text_widget.insert(tk.END, f'{i}. {combo}\n')
        else:
            # Fallback caso o widget não seja encontrado (não deve ocorrer em uso normal).
            messagebox.showerror("Erro Interno", f"Widget de texto não encontrado para {meal_type}")

    # --- Métodos Auxiliares ("Privados") ---

    def _generate_meal_plan_data(self, num_options=5):
        """
        Gera um dicionário com listas de opções de refeições para cada categoria.
        Utiliza as listas mestras de refeições da instância e seleciona `num_options`
        de cada, após embaralhá-las.
        """
        # Cria cópias das listas mestras para não alterar as originais.
        breakfasts_copy = list(self.all_breakfasts)
        lunches_copy = list(self.all_lunches)
        snacks_copy = list(self.all_snacks)
        dinners_copy = list(self.all_dinners)

        # Embaralha as cópias.
        random.shuffle(breakfasts_copy)
        random.shuffle(lunches_copy)
        random.shuffle(snacks_copy)
        random.shuffle(dinners_copy)

        # Retorna o dicionário com o número de opções especificado.
        return {
            'Café da Manhã': breakfasts_copy[:num_options],
            'Almoço': lunches_copy[:num_options],
            'Lanche da Tarde': snacks_copy[:num_options],
            'Jantar': dinners_copy[:num_options]
        }

    def _validate_positive_numeric_input(self, event, entry_var, entry_widget):
        """
        Valida se a entrada em um widget TEntry é um número positivo.
        Altera o estilo do widget para 'Error.TEntry' (fundo rosa) se inválido,
        ou para 'TEntry' (padrão) se válido.
        Chamado em eventos <FocusOut> e <KeyRelease> dos campos numéricos.
        """
        try:
            # Obtém o valor diretamente do widget para ter a entrada mais recente,
            # especialmente útil para o evento <KeyRelease>.
            value_str = entry_widget.get()

            # Se o campo estiver vazio, considera válido (permite apagar o campo).
            if not value_str:
                entry_widget.config(style="TEntry")
                return

            # Tenta converter para o tipo numérico apropriado.
            if isinstance(entry_var, tk.IntVar): # Para o campo Idade
                value = int(value_str)
            else: # Para os campos Peso e Altura (DoubleVar)
                value = float(value_str)

            # Verifica se o valor é positivo.
            if value > 0:
                entry_widget.config(style="TEntry") # Estilo padrão para válido.
            else:
                entry_widget.config(style="Error.TEntry") # Estilo de erro para não positivo.
        except (ValueError, tk.TclError): # Captura erros de conversão.
            entry_widget.config(style="Error.TEntry")


if __name__ == '__main__':
    app = NutritionApp()
    app.mainloop()
