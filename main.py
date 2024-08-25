import math
from enum import Enum


class Regione(Enum):
    EMILIA_ROMAGNA = 1


def calcola_inps(ral: float) -> float:
    if ral < 0.0:
        raise ValueError("Negative RAL")

    # percentuali a carico del lavoratore dipendente
    percentuale_fpld_ivs = 0.0919
    percentuale_cig = 0.003
    percentuale_fondo_residuale = 0.00267

    percentuale = percentuale_fpld_ivs + percentuale_cig + percentuale_fondo_residuale

    return ral * percentuale


def calcola_irpef(imponibile_annuale: float) -> float:
    if imponibile_annuale < 0.0:
        raise ValueError("Imponibile annuale negativo.")

    no_tax_area = 8_145.0
    if imponibile_annuale <= no_tax_area:
        return 0.0

    primo_scaglione = 28_000.0
    percentuale_primo_scaglione = 0.23
    if imponibile_annuale <= primo_scaglione:
        return imponibile_annuale * percentuale_primo_scaglione

    secondo_scaglione = 50_000.0
    percentuale_secondo_scaglione = 0.35
    if imponibile_annuale <= secondo_scaglione:
        return (primo_scaglione - no_tax_area) * percentuale_primo_scaglione + (
            imponibile_annuale - primo_scaglione
        ) * percentuale_secondo_scaglione

    percentuale_ultimo_scaglione = 0.43
    return (
        (primo_scaglione - no_tax_area) * percentuale_primo_scaglione
        + (secondo_scaglione - primo_scaglione) * percentuale_secondo_scaglione
        + (imponibile_annuale - secondo_scaglione) * percentuale_ultimo_scaglione
    )


def calcola_addizionale_regionale(imponibile_annuale: float) -> float:
    # assumiamo di essere in Emilia - Romagna
    if imponibile_annuale < 0.0:
        raise ValueError("Imponibile annuale negativo.")

    primo_scaglione = 15_000.0
    percentuale_primo_scaglione = 0.0133
    if imponibile_annuale <= primo_scaglione:
        return imponibile_annuale * percentuale_primo_scaglione

    secondo_scaglione = 28_000.0
    percentuale_secondo_scaglione = 0.0193
    if imponibile_annuale <= secondo_scaglione:
        return (
            primo_scaglione * percentuale_primo_scaglione
            + (imponibile_annuale - primo_scaglione) * percentuale_secondo_scaglione
        )

    terzo_scaglione = 50_000.0
    percentuale_terzo_scaglione = 0.0203
    if imponibile_annuale <= terzo_scaglione:
        return (
            primo_scaglione * percentuale_primo_scaglione
            + (secondo_scaglione - primo_scaglione) * percentuale_secondo_scaglione
            + (imponibile_annuale - secondo_scaglione) * percentuale_terzo_scaglione
        )

    percentuale_ultimo_scaglione = 0.0227
    return (
        primo_scaglione * percentuale_primo_scaglione
        + (secondo_scaglione - primo_scaglione) * percentuale_secondo_scaglione
        + (terzo_scaglione - secondo_scaglione) * percentuale_terzo_scaglione
        + (imponibile_annuale - terzo_scaglione) * percentuale_ultimo_scaglione
    )


def calcola_addizionale_comunale(imponibile_annuale: float) -> float:
    # assumiamo di essere a Bologna
    if imponibile_annuale < 0.0:
        raise ValueError("Imponibile annuale negativo.")

    return imponibile_annuale * 0.008


def calcola_detrazioni(imponibile_annuale: float) -> float:
    # assumiamo di essere lavoratori dipendenti
    if imponibile_annuale < 0.0:
        raise ValueError("Imponibile annuale negativo.")

    primo_scaglione = 15_000.0
    if imponibile_annuale <= primo_scaglione:
        return 1_955.0

    secondo_scaglione = 28_000.0
    if imponibile_annuale <= secondo_scaglione:
        return 1_910.0 + 1_190.0 * ((secondo_scaglione - imponibile_annuale) / 13_000.0)

    terzo_scaglione = 50_000.0
    if imponibile_annuale <= terzo_scaglione:
        return 1_910.0 * ((terzo_scaglione - imponibile_annuale) / 22_000.0)

    return 0.0


def breakdown_annuale(ral: float) -> None:
    ral_mensile = ral / 14.0
    ral_mensile_arrotondata = math.ceil(ral_mensile)
    print(f" RAL                 : {ral:.2f} €")
    print(f" RAL mensile         : {ral_mensile:.2f} €")
    print(f" RAL mensile arrot.  : {ral_mensile_arrotondata:.2f} €")

    inps = calcola_inps(ral)
    print(f" INPS annuale        : {inps:.2f} €")
    print(f" INPS mensile        : {(inps/14.0):.2f} €")

    imponibile_annuale = ral - inps

    irpef = calcola_irpef(imponibile_annuale)
    if ral <= 35_000.0:
        percentuale_esonero = (
            0.07
            if (ral_mensile_arrotondata <= 1_923.0)
            else (0.06 if ral_mensile_arrotondata <= 2_692.0 else 0.0)
        )
        print(f" Esonero IRPEF       : {(percentuale_esonero*100.0):.2f} %")

        esonero_mensile = ral_mensile_arrotondata * percentuale_esonero
        esonero_annuale = esonero_mensile * 12.0
        print(f" Esonero IRPEF annuale : {esonero_annuale:.2f} €")
        print(f" Esonero IRPEF mensile : {esonero_mensile:.2f} €")
        # sconto del 6%
        irpef = max(0.0, irpef - esonero_annuale)

    print(f" IRPEF annuale         : {irpef:.2f} €")
    print(f" IRPEF mensile         : {(irpef/12.0):.2f} €")

    detrazioni = calcola_detrazioni(imponibile_annuale) * 12.0 / 14.0
    print(f" Detrazioni annuali    : {detrazioni:.2f} €")
    print(f" Detrazioni mensili    : {(detrazioni/14.0):.2f} €")

    addizionale_regionale = calcola_addizionale_regionale(imponibile_annuale)
    print(
        f" Addizionale regionale Emilia-Romagna annuale : {addizionale_regionale:.2f} €"
    )
    print(
        f" Addizionale regionale Emilia-Romagna mensile : {(addizionale_regionale/12.0):.2f} €"
    )

    addizionale_comunale = calcola_addizionale_comunale(imponibile_annuale)
    print(f" Addizionale comunale Bologna annuale : {addizionale_comunale:.2f} €")
    print(
        f" Addizionale comunale Bologna mensile : {(addizionale_comunale / 12.0):.2f} €"
    )

    totale_imposte = max(
        0.0, irpef + addizionale_regionale + addizionale_comunale - detrazioni
    )

    print(f" Totale imposte annuale    : {totale_imposte:.2f} €")
    print(f" Totale imposte mensile    : {(totale_imposte / 14.0):.2f} €")
    print(f" Totale imposte %          : {((totale_imposte / ral) * 100.0):.2f} %")

    totale_trattenute = totale_imposte + inps

    print(f" Totale trattenute annuale : {totale_trattenute:.2f} €")
    print(f" Totale trattenute mensile : {(totale_trattenute / 14.0):.2f} €")

    print(f" Netto annuale             : {(ral - totale_trattenute):.2f} €")
    print(f" Netto mensile             : {((ral - totale_trattenute) / 14.0):.2f} €")


def breakdown_mensile(ral: float) -> None:
    ral_mensile = ral / 14.0
    ral_mensile_arrotondata = math.ceil(ral_mensile)
    # TODO


def main() -> None:
    ral = 30_000.0
    mensilita_aggiuntive = 2
    regione = Regione.EMILIA_ROMAGNA
    breakdown_annuale(ral)


if __name__ == "__main__":
    main()
