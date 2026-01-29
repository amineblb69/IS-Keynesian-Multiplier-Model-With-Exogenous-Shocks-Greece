import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import numpy as np



#---------------------------------------------------IMPORT VARIABLES EXOGENES

#Import du revenu disponible brut avant choc (Yd0)
revenu=pd.read_excel(io="data.xlsx",sheet_name="Revenu disponible brut").iloc[[7,15]]
revenu_dispo_brut=revenu.T.iloc[1:].reset_index(drop=True)
revenu_dispo_brut.columns = ['Date','Greece']
revenu_dispo_brut['Greece'] = pd.to_numeric(revenu_dispo_brut['Greece'], errors='coerce')
Yd0=revenu_dispo_brut['Greece']


#Import consommation(C)
conso=pd.read_excel(io="data.xlsx",sheet_name="Consommation").iloc[[7,15]]
consommation=conso.T.iloc[1:].reset_index(drop=True)
consommation.columns =['Date','Greece']
consommation['Greece'] = pd.to_numeric(consommation['Greece'], errors='coerce')
C=consommation['Greece']


#Import depenses gouvernementales 
depenses=pd.read_excel(io="data.xlsx",sheet_name="Dépenses publiques").iloc[[7,15]]
depenses_publiques=depenses.T.iloc[1:].reset_index(drop=True)
depenses_publiques.columns = ['Date','Greece']
depenses_publiques['Greece'] = pd.to_numeric(depenses_publiques['Greece'], errors='coerce')
G=depenses_publiques['Greece']


#Import investissement(I)
fbcf=pd.read_excel(io="data.xlsx",sheet_name="Investissement").iloc[[8,16]]
investissement=fbcf.T.iloc[1:].reset_index(drop=True)
investissement.columns = ['Date','Greece']
investissement['Greece'] = pd.to_numeric(investissement['Greece'], errors='coerce')
I=investissement['Greece']  


#Taux d'imposition suppose 
t=0.25


#---------------------------------------------------TRAITEMENT VARIABLES EXOGENES

#Calcul polynome 1er deg conso avant choc
polynome=np.polyfit(x=revenu_dispo_brut['Greece'],y=consommation['Greece'],deg=1)# np.polyfit aide obtenir un polynome du 1er degres de la forme y= ax + b a partir de la data
pente_conso_avantchoc=np.poly1d(polynome)#poly1d prends en entree les parametres du polynome et renvoie une fonction

c0=polynome[1]#consommation autonome
c1=polynome[0]#propension marginale a consommer

fonction2conso=f"y={round(c1,2)}x + ({round(c0,2)})"

print(fonction2conso)

#Calcul de la demande autonome
ZA=c0+I+G

#Moyenne Investissement et Depenses Gouvernementales
average_I=np.average(I)
average_G=np.average(G)


#---------------------------------------------------FONCTIONS PRINCIPALES
class formules_avantchoc():
    
    
    
    def fonction_consommation(c0, c1, Yd0=None, Y0=None, t=None):
        if Yd0 is not None:
            return c0 + c1 * Yd0
        elif Y0 is not None and t is not None:
            return c0 + c1 * (1 - t) * Y0
        else:
            raise ValueError("Yd ou (Y et t) doivent être fournis")

    def demande_globale(C,I,G):
        Z=C+I+G
        return Z

    def production(Yd0,t) :
        Y0 = Yd0 / (1 - t)
        return Y0

    def impots(Y0, Yd0, t=None):
        if t is None:
            t = 1 - (Yd0 / Y0)
        T = t * Y0
        return T
    
    def epargne(Yd0,C):
        S=Yd0-C
        return S
    
    def revenu_disponible(Y,t):
        Yd=Y*(1-t)
        return Yd
    
    Z=demande_globale(C,I,G)
    Y=Z
class formules_apreschoc():

    k=1/(1-c1*(1-t))#Multiplicateur Keynesien a partir des hypotheses 

    #Collecte des variables qui subissent un choc
    nb_variables_choc = 1
    variables_choc = []
    delta_choc=[]
    variables_valides = ['c0', 'I', 'G']

    
    #Application du choc
    for i in range(nb_variables_choc):
        variable = input(f"Entrez la variable exogène n°{i+1} ('c0','I','G') : ")
        if variable in variables_valides:
            variables_choc.append(variable)
            delta_choc.append(float(input("Entrez la fluctuation notée sur cette variable : ")))

        else:
            print(f" '{variable}' n'est pas une variable valide.")
        
    df = pd.DataFrame([delta_choc],columns=variables_choc)
    print(df)

    
    delta_ZA = 0
    c0t=c0
    It=I
    Gt=G

    if 'c0' in df.columns:
        delta_ZA += df['c0'].iloc[0]
        c0t=c0+df['c0'].iloc[0]
        
    if 'I' in df.columns:
        delta_ZA += df['I'].iloc[0]
        It=I+df['I'].iloc[0]

    if 'G' in df.columns:
        delta_ZA += df['G'].iloc[0]
        Gt=G+df['G'].iloc[0]
    
    

    print(f"Variation de la demande autonome: {delta_ZA}")
    print(f"Multiplicateur keynésien: {round(k,3)}")

    delta_Y = k * delta_ZA
    print(f"Le PIB (Y) et la demande globale (Z) ont variees de {delta_Y} unitees")
    
    #PIB production revenu avant choc
    Y0=formules_avantchoc.production(Yd0=Yd0,t=t)
    Yt=Y0+delta_Y

    if abs(delta_Y) < 1e-10:  # 0 Proche de zéro
        Yt = Y0
        Ydt = Yd0
        Ct = C
        Zt = formules_avantchoc.Z
        ZAt = ZA
    else:
        Yt = Y0 + delta_Y
        # Revenu disponible Ydt apres choc
        Ydt = formules_avantchoc.revenu_disponible(Y=Yt, t=t)
        #Calcul demande autonome apres choc
        ZAt = c0t + It + Gt
        #Calcul de la consommation Ct apres choc
        Ct = formules_avantchoc.fonction_consommation(c0=c0t, c1=c1, Yd0=Ydt)
        #Calcul demande globale Zt apres choc
        Zt = formules_avantchoc.demande_globale(C=Ct, I=It, G=Gt)
'''
    print(f"Demande globale Z avant choc ({formules_avantchoc.Z[0]}),   Demande globale Z apres choc ({Zt[0]})")
    print(f"Production globale avant choc ({Y0[0]}), Production globale apres choc ({Yt[0]})")
    print(f"Revenu disponible avant choc ({Yd0[0]}), Revenu disponible apres choc ({Ydt[0]})")
    print(f"Investissement avant choc({I[0]}),\nDepenses gouvernementales avant choc ({G[0]})")
    print(f"Consommation avant choc ({C[0]}),Consommation apres choc ({Ct[0]}),\n pmc avant choc ({c1}), conso autonome avant choc ({c0}), conso autonome apres choc ({c0t})")
'''
    
    

#---------------------------------------------------TRAITEMENT VARIABLES ENDOGENES

#Calcul du taux d'investissement(Part de l'investissement des entreprises dans le PIB)
taux_I=(I/formules_apreschoc.Y0)

#Calcul du taux de depenses publiques (Part des depenses publiques dans le PIB)
taux_G=(G/formules_apreschoc.Y0)


#Calcul epargne pente et coeff avant choc
epargne_grecque=formules_avantchoc.epargne(revenu_dispo_brut['Greece'],consommation['Greece'])
S=epargne_grecque
poly_epargne=np.polyfit(x=revenu_dispo_brut['Greece'].values, y=epargne_grecque.values, deg=1)
pente_epargne=np.poly1d(poly_epargne)


s0=poly_epargne[1]#epargne autonome
s1=poly_epargne[0]#propension marginale a epargner 

fonction_epargne_avantchoc=f"y={round(s1,2)}x +({round(s0,2)})"

#Calcul epargne pente et coeff apres choc

epargne_grecque_apreschoc=formules_avantchoc.epargne(Yd0=formules_apreschoc.Ydt, C=formules_apreschoc.Ct)

poly_epargne_apreschoc=np.polyfit(x=formules_apreschoc.Yt.values, y=epargne_grecque_apreschoc.values, deg=1)
pente_epargne_apreschoc=np.poly1d(poly_epargne_apreschoc)

s0t=poly_epargne_apreschoc[1]
s1t=poly_epargne_apreschoc[0]

fonction_epargne_apreschoc=f"y={round(s1t,2)}x +{round(s0t,2)}"

#Calcul pente demande autonome apres choc
polynome_demande_auto_apreschoc = np.polyfit(x=formules_apreschoc.Yt , y=formules_apreschoc.ZAt ,deg=1)
pente_demande_auto_apreschoc=np.poly1d(polynome_demande_auto_apreschoc)


#---------------------------------------------------FIGURES
#Avant Choc
class figures() :
    #---------------------------------------------------FIGURE 1 : Conso, Epargne, Demande Globale avant choc

    #Creation figure de deux graphs
    fig1, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(25, 5))

    # Calcul ligne de régression pour consommation
    x_line = np.linspace(revenu_dispo_brut['Greece'].min(), revenu_dispo_brut['Greece'].max(), 100)
    y_line_conso_avantchoc = pente_conso_avantchoc(x_line)

    # Graph 1 : Consommation/Revenu avant choc
    ax1.scatter(x=revenu_dispo_brut['Greece'], y=consommation['Greece'], label='Données', color='blue')
    ax1.plot(x_line, y_line_conso_avantchoc, color='red', linewidth=2, label=fonction2conso)
    ax1.set_xlabel("Revenu disponible brut (en millions d'euros)")
    ax1.set_ylabel("Consommation des ménages (en millions d'euros)")
    ax1.set_title("Consommation et revenu disponible Grecque")
    ax1.legend()
    ax1.grid(True)

    # Graph 2 : Épargne/Revenu avant choc
    y_line_epargne_avantchoc = pente_epargne(x_line)
    ax2.scatter(x=revenu_dispo_brut['Greece'], y=epargne_grecque, label='Données', color='green')
    ax2.plot(x_line, y_line_epargne_avantchoc, color='orange', linewidth=2, label=fonction_epargne_avantchoc)
    ax2.set_xlabel("Revenu disponible brut (en millions d'euros)")
    ax2.set_ylabel("Épargne (en millions d'euros)")
    ax2.set_title("Épargne et revenu disponible Grecque")
    ax2.legend()
    ax2.grid(True)

    # Calcul de la plage de Y
    Y_range = np.linspace(0, formules_apreschoc.Y0.max() * 1.2, 100)
    
    # Demande globale avant choc: Z = c0 + c1(1-t)Y + I + G
    pente_Z = c1 * (1 - t)
    intercept_avant = c0 + I.iloc[0] + G.iloc[0]
    Z_avant = pente_Z * Y_range + intercept_avant
    formule_Z_avant = f"y={round(pente_Z, 2)}x + ({round(intercept_avant, 2)})"

    # Ligne d'équilibre 45° (Z = Y)
    ax3.plot(Y_range, Y_range, 'k--', linewidth=1.5, label="Droite d'équilibre Z=Y")

    # Demande globale avant choc
    ax3.plot(Y_range, Z_avant, color='blue', linewidth=2, label=formule_Z_avant)


    ax3.set_xlabel("Revenu, Production (Y)")
    ax3.set_ylabel("Demande Z, Production Y")
    ax3.set_title("Équilibre keynésien : Demande globale et Production")
    ax3.legend()
    ax3.grid(True)
    
    
    plt.tight_layout()
    plt.show()

    # ---------------------------------------------------FIGURE 2 : I et G avec les moyennes

    fig2, ((ax4, ax5),(ax6, ax7)) = plt.subplots(nrows=2, ncols=2, figsize=(32, 10))

    x_dates = investissement['Date']
    x_dates_G = depenses_publiques['Date']

    ax4.plot(x_dates, I, marker='o', linestyle='-', color='orange', label='Investissement (I)')
    ax4.axhline(average_I, color='black', linestyle='--', label=f'Moyenne I = {average_I:.2f}')
    ax4.set_title('Investissement Grecque')
    ax4.set_xlabel('Date')
    ax4.set_ylabel("Valeur (millions d'euros)")
    ax4.legend()
    ax4.grid(True)

    ax5.plot(x_dates_G, G, marker='o', linestyle='-', color='red', label='Dépenses publiques (G)')
    ax5.axhline(average_G, color='black', linestyle='--', label=f'Moyenne G = {average_G:.2f}')
    ax5.set_title('Dépenses publiques ')
    ax5.set_xlabel('Date')
    ax5.set_ylabel("Valeur (millions d'euros)")
    ax5.legend()
    ax5.grid(True)

    ax6.plot(x_dates,taux_I, linestyle='--', color='orange', label="Taux d'investissement")
    ax6.set_title("Taux d'investissement")
    ax6.set_xlabel("Date")
    ax6.set_ylabel("Taux")
    ax6.grid(True)

    ax7.plot(x_dates,taux_G, linestyle='--', color='red', label="Taux de dépenses publiques")
    ax7.set_title("Taux de dépenses publiques")
    ax7.set_xlabel("Date")
    ax7.set_ylabel("Taux")
    ax7.grid(True)

    plt.tight_layout()
    plt.show()

    # ---------------------------------------------------FIGURE 3 : comme Figure 1 avec superposition données après choc
    
    fig3, (ax4b, ax5b, ax6b) = plt.subplots(1, 3, figsize=(25, 5))

    # --- Graphique Consommation (avant)
    ax4b.scatter(x=revenu_dispo_brut['Greece'], y=consommation['Greece'], label='Données avant choc', color='tab:blue')
    ax4b.plot(x_line, y_line_conso_avantchoc, color='red', linewidth=2, label=fonction2conso)

    # superposer la consommation après choc si disponible
    
    poly_conso_apres = np.polyfit(x=formules_apreschoc.Ydt.values, y=formules_apreschoc.Ct.values, deg=1)
    pente_conso_apreschoc = np.poly1d(poly_conso_apres)
    x_line_post = np.linspace(formules_apreschoc.Ydt.min(), formules_apreschoc.Ydt.max(), 100)
    y_line_conso_apres = pente_conso_apreschoc(x_line_post)
    ax4b.plot(x_line_post, y_line_conso_apres, color='darkred', linewidth=2, label='Régression après choc')
    #ax4b.scatter(x=formules_apreschoc.Ydt, y=formules_apreschoc.Ct, label='Données après choc', color='darkblue')

    ax4b.set_xlabel("Revenu disponible brut (en millions d'euros)")
    ax4b.set_ylabel("Consommation des ménages (en millions d'euros)")
    ax4b.set_title("Consommation et revenu disponible : avant et après choc")
    ax4b.legend()
    ax4b.grid(True)

    # --- Graphique Épargne (avant)
    ax5b.scatter(x=revenu_dispo_brut['Greece'], y=epargne_grecque, label='Données avant choc', color='green')
    ax5b.plot(x_line, y_line_epargne_avantchoc, color='orange', linewidth=2, label=fonction_epargne_avantchoc)

    # superposer l'épargne après choc si disponible


    x_line_s_after = np.linspace(formules_apreschoc.Yt.min(), formules_apreschoc.Yt.max(), 100)
    y_line_s_after = pente_epargne_apreschoc(x_line_s_after)
    ax5b.plot(x_line_s_after, y_line_s_after, color='darkorange', linewidth=2, label='Régression épargne après choc')
    #ax5b.scatter(x=formules_apreschoc.Yt, y=epargne_grecque_apreschoc, label='Données après choc', color='darkgreen')
    
    ax5b.set_xlabel("Revenu disponible brut (en millions d'euros)")
    ax5b.set_ylabel("Épargne (en millions d'euros)")
    ax5b.set_title("Épargne et revenu disponible : avant et après choc")
    ax5b.legend()
    ax5b.grid(True)

    # --- Graphique Demande globale (avant)
    ax6b.plot(Y_range, Y_range, 'k--', linewidth=1.5, label="Droite d'équilibre Z=Y")
    ax6b.plot(Y_range, Z_avant, color='blue', linewidth=2, label=formule_Z_avant)

    # Demande globale après choc: Z = c0t + c1(1-t)Y + It + Gt
    intercept_apres = formules_apreschoc.c0t + formules_apreschoc.It.iloc[0] + formules_apreschoc.Gt.iloc[0]
    Z_apres = pente_Z * Y_range + intercept_apres  # pente_Z reste la même : c1(1-t)
    formule_Z_apres = f"y={round(pente_Z, 2)}x + ({round(intercept_apres, 2)})"

    ax6b.plot(Y_range, Z_apres, color='darkblue', linewidth=2, label=formule_Z_apres)

    
    ax6b.set_xlabel("Revenu, Production (Y)")
    ax6b.set_ylabel("Demande Z, Production Y")
    ax6b.set_title("Équilibre keynésien : avant et après choc")
    ax6b.legend()
    ax6b.grid(True)


    plt.tight_layout()
    plt.show()
