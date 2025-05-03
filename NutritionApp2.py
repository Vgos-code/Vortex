import tkinter as tk
from tkinter import ttk, messagebox
import random

# Cálculos nutricionais

def calculate_bmr(weight, height, age, sex):
    """
    Calcula o Metabolismo Basal (BMR) usando a equação de Mifflin-St Jeor.
    Homens: 10*peso + 6.25*altura - 5*idade + 5
    Mulheres: 10*peso + 6.25*altura - 5*idade - 161
    """
    sex = sex.strip().lower()
    if sex not in ('m', 'f'):
        raise ValueError('Sexo deve ser "m" (masculino) ou "f" (feminino)')
    if sex == 'm':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161


def recommended_calories(bmr, activity_level):
    """
    Ajusta o BMR para calorias diárias com base no nível de atividade física.
    Levels: sedentário, leve, moderado, ativo, muito ativo
    """
    levels = {
        'sedentário': 1.2,
        'leve': 1.375,
        'moderado': 1.55,
        'ativo': 1.725,
        'muito ativo': 1.9
    }
    key = activity_level.strip().lower()
    if key not in levels:
        raise ValueError('Nível de atividade inválido')
    return bmr * levels[key]


def calculate_bmi(weight, height):
    """
    Calcula o IMC.
    """
    return weight / (height / 100) ** 2


def bmi_classification(bmi):
    """
    Classificação do IMC.
    """
    if bmi < 18.5:
        return 'Abaixo do peso'
    elif bmi < 25:
        return 'Peso normal'
    elif bmi < 30:
        return 'Sobrepeso'
    else:
        return 'Obesidade'


def macro_distribution(calories):
    """
    Distribuição padrão de macronutrientes:
     - Carboidratos: 50%
     - Proteínas: 20%
     - Gorduras: 30%
    Converte calorias em gramas.
    """
    carbs_cal = calories * 0.50
    protein_cal = calories * 0.20
    fat_cal = calories * 0.30
    # 1g carboidrato = 4 kcal, proteína = 4 kcal, gordura = 9 kcal
    carbs_g = carbs_cal / 4
    protein_g = protein_cal / 4
    fat_g = fat_cal / 9
    return round(carbs_g), round(protein_g), round(fat_g)


def water_intake(weight):
    """
    Recomenda ingestão de água em litros (35 ml por kg de peso).
    """
    return round(weight * 35 / 1000, 2)


def generate_meal_plan():
    """
    Gera um plano de refeições com 20 combinações para cada refeição.
    """
    breakfasts = [
        'Omelete de claras com espinafre e tomate',
        'Iogurte grego com granola sem açúcar e frutas vermelhas',
        'Vitamina de banana com aveia e chia',
        'Panqueca de aveia com mel e banana',
        'Tapioca com queijo cottage e peito de peru',
        'Pão integral com abacate e ovo poché',
        'Mingau de aveia com maçã e canela',
        'Smoothie verde com couve, abacaxi e gengibre',
        'Crepioca de frango desfiado',
        'Waffle integral com iogurte e morango',
        'Sanduíche de pão integral com ricota e peito de peru',
        'Parfait de iogurte, chia e kiwi',
        'Wrap de alface com ricota temperada',
        'Overnight oats com leite de amêndoas e blueberries',
        'Pão sírio integral com homus e cenoura ralada',
        'Muffin integral de banana e aveia',
        'Ovos mexidos com cogumelos e espinafre',
        'Vitaminado de mamão e linhaça',
        'Crepioca de banana com canela',
        'Smoothie bowl de frutas vermelhas e granola'
    ]

    lunches = [
        'Peito de frango grelhado, arroz integral e brócolis',
        'Filé de peixe assado, purê de batata doce e salada verde',
        'Carne magra refogada com legumes e quinoa',
        'Salada de atum com grão de bico e vinagrete de limão',
        'Frango ao curry com legumes no vapor',
        'Tacos de alface com carne moída magra',
        'Espaguete de abobrinha ao pesto',
        'Salada de lentilhas com cenoura e pepino',
        'Strogonoff de frango light com arroz integral',
        'Quiche de espinafre light com salada de folhas',
        'Tilápia grelhada com legumes assados',
        'Fricassê de grão de bico com espinafre',
        'Panqueca americana de aveia com recheio de frango',
        'Berinjela recheada com carne magra e tomate',
        'Arroz de couve-flor com frango desfiado',
        'Bife magro grelhado com mandioca cozida',
        'Feijão tropeiro light com couve e ovo cozido',
        'Tabule de quinoa com ervas finas',
        'Wrap integral com peito de peru e salada',
        'Sopa de legumes com carne magra desfiada'
    ]

    snacks = [
        'Banana com pasta de amendoim',
        'Maçã fatiada com canela e nozes',
        'Iogurte natural com sementes de abóbora',
        'Mix de castanhas e passas',
        'Barrinha de cereal integral caseira',
        'Palitos de cenoura e pepino com homus',
        'Torrada integral com queijo branco',
        'Vitamina de abacate com cacau',
        'Smoothie de morango e chia',
        'Cookie integral de aveia e banana',
        'Pipoca de panela sem óleo',
        'Pêssego com iogurte grego',
        'Uvas congeladas',
        'Chips de batata doce assada',
        'Bolinho de batata doce e aveia',
        'Tapioca simples com queijo de minas',
        'Melancia em cubos',
        'Vitamina de laranja e cenoura',
        'Geleia de fruta sem açúcar em torrada integral',
        'Cereal integral com leite desnatado'
    ]

    dinners = [
        'Salmão grelhado com aspargos ao vapor',
        'Tilápia ao forno com purê de mandioquinha',
        'Frango assado com abóbora e couve',
        'Sopa cremosa de cenoura e gengibre',
        'Carne de panela magra com batata doce',
        'Omelete de legumes variados',
        'Peito de peru grelhado com salada de rúcula',
        'Berinjela à parmegiana light',
        'Salada de folhas verdes com ovo cozido',
        'Quinoa com legumes e grão de bico',
        'Abobrinha recheada com cogumelos',
        'Espaguete de pupunha ao molho de tomate',
        'Sardinha grelhada com salada de tomate',
        'Quibe assado de forno com salada',
        'Camarão ao alho e óleo com legumes',
        'Sopa de abóbora com sementes de girassol',
        'Carne moída magra refogada com vagem',
        'Salmão ao vapor com brócolis',
        'Wrap de alface com frango grelhado',
        'Panqueca integral de espinafre'
    ]

    random.shuffle(breakfasts)
    random.shuffle(lunches)
    random.shuffle(snacks)
    random.shuffle(dinners)

    return {
        'Café da Manhã': breakfasts,
        'Almoço': lunches,
        'Lanche da Tarde': snacks,
        'Jantar': dinners
    }


class NutritionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Aplicativo de Apoio para Nutricionistas')
        self.geometry('800x800')
        self.resizable(True, True)

        # Variáveis de entrada
        self.weight_var = tk.DoubleVar()
        self.height_var = tk.DoubleVar()
        self.age_var = tk.IntVar()
        self.sex_var = tk.StringVar(value='m')
        self.activity_var = tk.StringVar(value='Sedentário')

        # Frame de entrada
        input_frame = ttk.LabelFrame(self, text='Dados do Paciente', padding=10)
        input_frame.pack(fill='x', padx=10, pady=10)

        row = 0
        ttk.Label(input_frame, text='Peso (kg):').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.weight_var).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        ttk.Label(input_frame, text='Altura (cm):').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.height_var).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        ttk.Label(input_frame, text='Idade (anos):').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.age_var).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        ttk.Label(input_frame, text='Sexo:').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        sex_frame = ttk.Frame(input_frame)
        sex_frame.grid(row=row, column=1, padx=5, pady=5)
        ttk.Radiobutton(sex_frame, text='Masculino', variable=self.sex_var, value='m').pack(side='left')
        ttk.Radiobutton(sex_frame, text='Feminino', variable=self.sex_var, value='f').pack(side='left')
        row += 1
        ttk.Label(input_frame, text='Nível de Atividade:').grid(row=row, column=0, sticky='w', padx=5, pady=5)
        activity_options = ['Sedentário', 'Leve', 'Moderado', 'Ativo', 'Muito Ativo']
        activity_combo = ttk.Combobox(input_frame, values=activity_options, state='readonly', textvariable=self.activity_var)
        activity_combo.grid(row=row, column=1, padx=5, pady=5)
        row += 1

        # Botão de cálculo
        ttk.Button(self, text='Calcular Plano', command=self.calculate).pack(pady=10)

        # Frame de resultados
        self.results_frame = ttk.LabelFrame(self, text='Resultados', padding=10)
        self.results_frame.pack(fill='x', padx=10, pady=10)

        self.bmr_label = ttk.Label(self.results_frame, text='Metabolismo Basal: -')
        self.bmr_label.pack(anchor='w')
        self.cal_label = ttk.Label(self.results_frame, text='Calorias Recomendadas: -')
        self.cal_label.pack(anchor='w')
        self.bmi_label = ttk.Label(self.results_frame, text='IMC: -')
        self.bmi_label.pack(anchor='w')
        self.class_label = ttk.Label(self.results_frame, text='Classificação IMC: -')
        self.class_label.pack(anchor='w')
        self.macro_label = ttk.Label(self.results_frame, text='Macros (g): Carbs -, Prot -, Gord -')
        self.macro_label.pack(anchor='w')
        self.water_label = ttk.Label(self.results_frame, text='Ingestão de água (L/dia): -')
        self.water_label.pack(anchor='w')

        # Notebook para plano de refeições
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.meal_texts = {}
        for meal in ['Café da Manhã', 'Almoço', 'Lanche da Tarde', 'Jantar']:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=meal)
            text = tk.Text(frame, wrap='word')
            text.pack(side='left', fill='both', expand=True)
            scrollbar = ttk.Scrollbar(frame, orient='vertical', command=text.yview)
            scrollbar.pack(side='right', fill='y')
            text.configure(yscrollcommand=scrollbar.set)
            self.meal_texts[meal] = text

    def calculate(self):
        try:
            weight = self.weight_var.get()
            height = self.height_var.get()
            age = self.age_var.get()
            sex = self.sex_var.get()
            activity = self.activity_var.get()

            bmr = calculate_bmr(weight, height, age, sex)
            calories = recommended_calories(bmr, activity)
            bmi = calculate_bmi(weight, height)
            classification = bmi_classification(bmi)
            carbs, prot, fat = macro_distribution(calories)
            water = water_intake(weight)
            plan = generate_meal_plan()

            # Atualizar labels
            self.bmr_label.config(text=f'Metabolismo Basal: {bmr:.0f} kcal/dia')
            self.cal_label.config(text=f'Calorias Recomendadas (TDEE): {calories:.0f} kcal/dia')
            self.bmi_label.config(text=f'IMC: {bmi:.1f}')
            self.class_label.config(text=f'Classificação IMC: {classification}')
            self.macro_label.config(text=f'Macros (g): Carbs {carbs}, Prot {prot}, Gord {fat}')
            self.water_label.config(text=f'Ingestão de água (L/dia): {water}')

            # Preencher plano de refeições
            for meal, text_widget in self.meal_texts.items():
                text_widget.delete('1.0', tk.END)
                combos = plan.get(meal, [])
                for i, combo in enumerate(combos, 1):
                    text_widget.insert(tk.END, f'{i}. {combo}\n')

        except Exception as e:
            messagebox.showerror('Erro de Entrada', str(e))


if __name__ == '__main__':
    app = NutritionApp()
    app.mainloop()
