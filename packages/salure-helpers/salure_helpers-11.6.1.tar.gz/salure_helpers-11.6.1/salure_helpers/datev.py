import pandas as pd
from datetime import datetime


def check_if_column_in_dataset(required_columns_subset: list, df_columns: pd.DataFrame.index):
    if any(column in required_columns_subset for column in df_columns):
        if not all(column in df_columns for column in required_columns_subset):
            missing_columns = []
            for column in required_columns_subset:
                if column not in df_columns:
                    missing_columns.append(column)
            raise Exception(f"You are missing: {missing_columns} from the following columns : {','.join(required_columns_subset)}")
        else:
            return True
    else:
        return False


class Datev(object):
    def __init__(self, berater_nr: int, mandanten_nr: int):
        self.berater_nr = berater_nr
        self.mandanten_nr = mandanten_nr

    def export_to_template(self, df: pd.DataFrame, filepath: str, valid_from: str = datetime.today().strftime('%d.%m.%Y'), use_alternative_employee_number: bool = False):

        required_fields = []
        for field in required_fields:
            if field not in df.columns:
                return f'Column {field} is required. Required columns are: {tuple(required_fields)}'

        template_headers = f""" [Allgemein]
                                Ziel=LODAS
                                Version_SST=1.0
                                Version_DB=10.62
                                BeraterNr={self.berater_nr}
                                MandantenNr={self.mandanten_nr}
                                Kommentarzeichen=*
                                Feldtrennzeichen=;
                                Zahlenkomma=,
                                Datumsformat=TT/MM/JJJJ
                                StammdatenGueltigAb={valid_from}
                                {'BetrieblichePNrVerwenden=Ja' if use_alternative_employee_number else 'BetrieblichePNrVerwenden=Nein'}"""
        template_description = """[Satzbeschreibung]"""
        template_body = """[Stammdaten]"""

        # This is the custom export that is different per customer. This one makes a txt for every new employee and adds information in the template with a string format.
        # template = self.get_template(valid_from, use_alternative_employee_number)
        for index, dfrow in df.iterrows():
            with open(f'{filepath}.txt', 'w', encoding="latin-1", newline='\r\n') as file:
                description = [template_description]
                body = [template_body]

                required_columns_subset = ['lastname', 'firstname', 'birthname', 'street', 'housenumber', 'postalcode', 'city']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"100;{dfrow['employee_id']};{dfrow['lastname']};{dfrow['firstname']};{dfrow['birthname']};{dfrow['street']};{dfrow['housenumber']};{dfrow['postalcode']};{dfrow['city']};")
                    body.append(
                        f"100;u_lod_psd_mitarbeiter;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};duevo_familienname#psd;duevo_vorname#psd;gebname#psd;adresse_strassenname#psd;adresse_strasse_nr#psd;adresse_plz#psd;adresse_ort#psd;")

                required_columns_subset = ['date_of_birth', 'place_of_birth', 'country_of_birth', 'gender', 'social_security_number', 'nationality']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(
                        f"101;u_lod_psd_mitarbeiter;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};geburtsdatum_ttmmjj#psd;gebort#psd;geburtsland#psd;geschlecht#psd;sozialversicherung_nr#psd;staatsangehoerigkeit#psd;")
                    body.append(f"101;{dfrow['employee_id']};{dfrow['date_of_birth']};{dfrow['place_of_birth']};{dfrow['country_of_birth']};{dfrow['gender']};{dfrow['social_security_number']};{dfrow['nationality']};")

                required_columns_subset = ['iban', 'bic']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"102;u_lod_psd_ma_bank;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};ma_iban#psd;ma_bic#psd;ma_bank_zahlungsart#psd;")
                    body.append(f"102;{dfrow['employee_id']};{dfrow['iban']};{dfrow['bic']};5;")

                required_columns_subset = ['disabled', 'type_of_employee']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"103;u_lod_psd_mitarbeiter;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};schwerbeschaedigt#psd;mitarbeitertyp#psd;")
                    body.append(f"103;{dfrow['employee_id']};{dfrow['disabled']};{dfrow['type_of_employee']};")

                required_columns_subset = ['costcenter', 'costcenter_percentage']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"104;u_lod_psd_kstellen_verteil;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};kostenstelle#psd;prozentsatz_kst#psd;")
                    body.append(f"104;{dfrow['employee_id']};{dfrow['costcenter']};{dfrow['costcenter_percentage']};")
                    description.append(f"503;u_lod_psd_taetigkeit;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};stammkostenstelle#psd;")
                    body.append(f"503;{dfrow['employee_id']};{dfrow['costcenter']};")

                required_columns_subset = ['costcarrier', 'costcarrier_percentage']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"105;u_lod_psd_ktraeger_verteil;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};kostentraeger#psd;prozentsatz_ktr#psd;")
                    body.append(f"105;{dfrow['employee_id']};{dfrow['costcarrier']};{dfrow['costcarrier_percentage']};")

                required_columns_subset = ['date_in_service', 'payment_type']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"200;u_lod_psd_mitarbeiter;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};ersteintrittsdatum#psd;vorweg_abr_abruf_termin_kz#psd;")
                    body.append(f"200;{dfrow['employee_id']};{dfrow['date_in_service']};{dfrow['payment_type']};")

                required_columns_subset = ['first_day_of_employment']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"201;u_lod_psd_beschaeftigung;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};eintrittdatum#psd;")
                    body.append(f"201;{dfrow['employee_id']};{dfrow['first_day_of_employment']};")

                required_columns_subset = ['salary_amount', 'tracking_number']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"240;u_lod_psd_festbezuege;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};betrag#psd;festbez_id#psd;intervall#psd;kuerzung#psd;kz_monatslohn#psd;lohnart_nr#psd;")
                    body.append(f"240;{dfrow['employee_id']};{dfrow['salary_amount']};{dfrow['tracking_number']};0;{dfrow['discount'] if 'discount' in dfrow else 0};;200;")

                required_columns_subset = ['company_bicycle_amount']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"241;u_lod_psd_festbezuege;pnr_betriebliche#psd;betrag#psd;festbez_id#psd;intervall#psd;kuerzung#psd;kz_monatslohn#psd;lohnart_nr#psd;")
                    body.append(f"241;{dfrow['employee_id']};{dfrow['company_bicycle_amount']};99;0;1;;233;")

                required_columns_subset = ['hourly_wage']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"262;u_lod_psd_lohn_gehalt_bezuege;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};std_lohn_1#psd;")
                    body.append(f"262;{dfrow['employee_id']};{dfrow['hourly_wage']};")

                required_columns_subset = ['insurancefund_number', 'unemployment_insurance', 'health_insurance', 'healthcare_insurance', 'pension_insurance']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"287;u_lod_psd_sozialversicherung;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};kk_nr#psd;av_bgrs#psd;kv_bgrs#psd;pv_bgrs#psd;rv_bgrs#psd;uml_schluessel#psd;")
                    body.append(f"287;{dfrow['employee_id']};{dfrow['insurancefund_number']};{dfrow['unemployment_insurance']};{dfrow['health_insurance']};{dfrow['healthcare_insurance']};{dfrow['pension_insurance']};2;")

                required_columns_subset = ['mandatory_insurance', 'hourly_wager']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"292;u_lod_psd_sv_unfall;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};uv_kz_pflichtig#psd;uv_kz_stundenerm#psd;")
                    body.append(f"292;{dfrow['employee_id']};{dfrow['mandatory_insurance']};{dfrow['hourly_wager']};")

                required_columns_subset = ['person_group', 'position', 'place_of_work', 'job_performed', 'job_performed_description', 'highest_degree', 'highest_training']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(
                        f"300;u_lod_psd_taetigkeit;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};persgrs#psd;berufsbezeichnung#psd;beschaeft_nr#psd;ausg_taetigkeit#psd;ausg_taetigkeit_lfdnr#psd;schulabschluss#psd;ausbildungsabschluss#psd;")
                    body.append(f"300;{dfrow['employee_id']};{dfrow['person_group']};{dfrow['position']};{dfrow['place_of_work']};{dfrow['job_performed']};{dfrow['job_performed_description']};{dfrow['highest_degree']};{dfrow['highest_training']};")

                required_columns_subset = ['type_of_contract', 'employee_type']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"400;u_lod_psd_taetigkeit;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};arbeitnehmerueberlassung#psd;vertragsform#psd;rv_beitragsgruppe#psd;")
                    body.append(f"400;{dfrow['employee_id']};0;{dfrow['type_of_contract']};{dfrow['employee_type']};")

                required_columns_subset = ['tax_class', 'main_employer', 'religion']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"701;u_lod_psd_steuer;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};st_klasse#psd;faktor#psd;kfb_anzahl#psd;els_2_haupt_ag_kz#psd;konf_an#psd;")
                    body.append(f"701;{dfrow['employee_id']};{dfrow['tax_class']};;;{dfrow['main_employer']};{dfrow['religion']};")

                required_columns_subset = ['taxnumber']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"702;u_lod_psd_steuer;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};identifikationsnummer#psd;")
                    body.append(f"702;{dfrow['employee_id']};{dfrow['taxnumber']};")

                required_columns_subset = ['hours_per_week', 'hours_monday', 'hours_tuesday', 'hours_wednesday', 'hours_thursday', 'hours_friday', 'hours_saturday', 'hours_sunday']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(
                        f"800;u_lod_psd_arbeitszeit_regelm;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};az_wtl_indiv#psd;regelm_az_mo#psd;regelm_az_di#psd;regelm_az_mi#psd;regelm_az_do#psd;regelm_az_fr#psd;regelm_az_sa#psd;regelm_az_so#psd;")
                    body.append(
                        f"800;{dfrow['employee_id']};{dfrow['hours_per_week']};{dfrow['hours_monday']};{dfrow['hours_tuesday']};{dfrow['hours_wednesday']};{dfrow['hours_thursday']};{dfrow['hours_friday']};{dfrow['hours_saturday']};{dfrow['hours_sunday']};")

                required_columns_subset = ['yearly_vacation_hours']
                if check_if_column_in_dataset(required_columns_subset, df.columns):
                    description.append(f"801;u_lod_psd_arbeitszeit_regelm;{'pnr_betriebliche#psd' if use_alternative_employee_number else 'pnr#psd'};url_tage_jhrl#psd;")
                    body.append(f"801;{dfrow['employee_id']};{dfrow['yearly_vacation_hours']};")

                file.writelines([template_headers] + description + body)
