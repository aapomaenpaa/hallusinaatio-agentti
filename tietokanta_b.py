import sqlite3
import pandas as pd

KOODIT = {
    "surface_area": "pinta_ala",
    "inhabitants_total_he": "he_vakiy",
    "males_he": "he_miehet",
    "females_he": "he_naiset",
    "average_age_of_inhabitants_he": "he_kika",
    "aged_18_or_over_total_ko": "ko_ika18y",
    "basic_level_studies_ko": "ko_perus",
    "with_education_total_ko": "ko_koul",
    "matriculation_examination_ko": "ko_yliop",
    "vocational_diploma_ko": "ko_ammat",
    "academic_degree_lowest_level_tertiary_and_lower_university_level_degrees_ko": "ko_al_kork",
    "academic_degree_higher_university_level_degree_ko": "ko_yl_kork",
    "aged_18_or_over_total_hr": "hr_tuy",
    "average_income_of_inhabitants_hr": "hr_ktu",
    "median_income_of_inhabitants_hr": "hr_mtu",
    "inhabitants_belonging_to_the_lowest_income_category_hr": "hr_pi_tul",
    "inhabitants_belonging_to_the_middle_income_category_hr": "hr_ke_tul",
    "inhabitants_belonging_to_the_highest_income_category_hr": "hr_hy_tul",
    "accumulated_purchasing_power_of_inhabitants_hr": "hr_ovy",
    "households_total_te": "te_taly",
    "average_size_of_households_te": "te_takk",
    "average_floor_area_per_person_te": "te_as_valj",
    "one_person_households_te": "te_yks",
    "young_one_person_households_te": "te_nuor",
    "young_couples_without_children_te": "te_eil_np",
    "households_with_children_te": "te_laps",
    "households_with_small_children_te": "te_plap",
    "households_with_children_under_school_age_te": "te_aklap",
    "households_with_school_age_children_te": "te_klap",
    "households_with_teenagers_te": "te_teini",
    "one_parent_households_with_children_te": "te_yhlap",
    "adult_households_te": "te_aik",
    "pensioner_households_te": "te_elak",
    "households_living_in_owner_occupied_dwellings_te": "te_omis_as",
    "households_living_in_rented_dwellings_te": "te_vuok_as",
    "households_living_in_other_dwellings_te": "te_muu_as",
    "households_total_tr": "tr_kuty",
    "average_income_of_households_tr": "tr_ktu",
    "median_income_of_households_tr": "tr_mtu",
    "households_belonging_to_the_lowest_income_category_tr": "tr_pi_tul",
    "households_belonging_to_the_middle_income_category_tr": "tr_ke_tul",
    "households_belonging_to_the_highest_income_category_tr": "tr_hy_tul",
    "accumulated_purchasing_power_of_households_tr": "tr_ovy",
    "free_time_residences_ra": "ra_ke",
    "buildings_total_ra": "ra_raky",
    "other_buildings_ra": "ra_muut",
    "residential_buildings_ra": "ra_asrak",
    "dwellings_ra": "ra_asunn",
    "average_floor_area_per_dwelling_ra": "ra_as_kpa",
    "dwellings_in_small_houses_ra": "ra_pt_as",
    "dwellings_in_blocks_of_flats_ra": "ra_kt_as",
    "other_dwellings_ra": "ra_muu_as",
    "workplaces_total_tp": "tp_tyopy",
    "primary_production_tp": "tp_alku_a",
    "processing_tp": "tp_jalo_bf",
    "services_tp": "tp_palv_gu",
    "a_agriculture_forestry_and_fishing_tp": "tp_a_maat",
    "b_mining_and_quarrying_tp": "tp_b_kaiv",
    "c_manufacturing_tp": "tp_c_teol",
    "d_electricity_gas_steam_and_air_conditioning_supply_tp": "tp_d_ener",
    "e_water_supply_sewerage_waste_management_and_remediation_activities_tp": "tp_e_vesi",
    "f_construction_tp": "tp_f_rake",
    "g_wholesale_and_retail_trade_repair_of_motor_vehicles_and_motorcycles_tp": "tp_g_kaup",
    "h_transportation_and_storage_tp": "tp_h_kulj",
    "i_accommodation_and_food_service_activities_tp": "tp_i_majo",
    "j_information_and_communication_tp": "tp_j_info",
    "k_financial_and_insurance_activities_tp": "tp_k_raho",
    "l_real_estate_activities_tp": "tp_l_kiin",
    "m_professional_scientific_and_technical_activities_tp": "tp_m_erik",
    "n_administrative_and_support_service_activities_tp": "tp_n_hall",
    "o_public_administration_and_defence_compulsory_social_security_tp": "tp_o_julk",
    "p_education_tp": "tp_p_koul",
    "q_human_health_and_social_work_activities_tp": "tp_q_terv",
    "r_arts_entertainment_and_recreation_tp": "tp_r_taid",
    "s_other_service_activities_tp": "tp_s_muup",
    "t_activities_of_households_as_employers_undifferentiated_goods_and_services_producing_activities_of_households_for_own_use_tp": "tp_t_koti",
    "u_activities_of_extraterritorial_organisations_and_bodies_tp": "tp_u_kans",
    "x_industry_unknown_tp": "tp_x_tunt",
    "inhabitants_total_pt": "pt_vakiy",
    "employed_pt": "pt_tyoll",
    "unemployed_pt": "pt_tyott",
    "children_aged_0_to_14_pt": "pt_0_14",
    "students_pt": "pt_opisk",
    "pensioners_pt": "pt_elakel",
    "others_pt": "pt_muut",
}

yhteys = sqlite3.connect("paavo.db")
df = pd.read_sql("SELECT * FROM alueet", yhteys)
yhteys.close()

ilman_koodia = [s for s in df.columns if s not in KOODIT and s not in ["postinumero", "alue", "kunta"]]
print("Sarakkeet ilman koodia:", ilman_koodia)

df = df.rename(columns=KOODIT)

yhteys_b = sqlite3.connect("paavo_b.db")
df.to_sql("alueet", yhteys_b, if_exists="replace", index=False)

kuvaukset_b = pd.DataFrame({"sarake": list(KOODIT.values()), "kuvaus": ""})
kuvaukset_b.to_sql("sarakekuvaukset", yhteys_b, if_exists="replace", index=False)

print(pd.read_sql("SELECT * FROM alueet LIMIT 2", yhteys_b))
yhteys_b.close()