# import needed modules
import os
import pandas as pd

# specify the URL of the dataset
url = 'https://drive.google.com/uc?export=download&id=1P_oMc6gOBlhw6dY5PxaqxV2swdHMUooK'

# read the Excel file from the specified URL and select the second sheet
master_data = pd.read_excel(url, sheet_name=1)

# check for duplicates in the data frame
if master_data.duplicated().sum() > 0:
    print('WARNING: Data contains duplicate rows.')
else:
    print('No duplicate rows found.')

# check for null values in the data frame
if master_data.isnull().sum().sum() > 0:
    print('WARNING: Data contains null values.')
else:
    print('No null values found.')

# convert all column names to lowercase
master_data.columns = master_data.columns.str.lower()

# rename the 'ptid' column to 'id'
master_data = master_data.rename(columns={'ptid': 'id'})

# uppercase all string values in the dataframe
master_data = master_data.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# create separate dataframes for different buckets
demographic_details = master_data[['id', 'persistency_flag', 'gender', 'race', 'ethnicity', 'region', 'age_bucket']]
provider_attributes = master_data[['id', 'persistency_flag', 'ntm_speciality', 'ntm_specialist_flag', 'ntm_speciality_bucket', 'idn_indicator']]
clinical_factors = master_data[['id', 'persistency_flag', 'gluco_record_prior_ntm', 'gluco_record_during_rx', 'dexa_freq_during_rx', 'dexa_during_rx', 'frag_frac_prior_ntm', 'frag_frac_during_rx', 'risk_segment_prior_ntm', 'tscore_bucket_prior_ntm', 'risk_segment_during_rx', 'tscore_bucket_during_rx', 'change_t_score', 'change_risk_segment', 'adherent_flag', 'injectable_experience_during_rx']]
comorbidity_details = master_data[['id', 'persistency_flag', 'comorb_encounter_for_screening_for_malignant_neoplasms', 'comorb_encounter_for_immunization', 'comorb_encntr_for_general_exam_w_o_complaint,_susp_or_reprtd_dx', 'comorb_vitamin_d_deficiency', 'comorb_other_joint_disorder_not_elsewhere_classified', 'comorb_encntr_for_oth_sp_exam_w_o_complaint_suspected_or_reprtd_dx', 'comorb_long_term_current_drug_therapy', 'comorb_dorsalgia', 'comorb_personal_history_of_other_diseases_and_conditions', 'comorb_other_disorders_of_bone_density_and_structure', 'comorb_disorders_of_lipoprotein_metabolism_and_other_lipidemias', 'comorb_osteoporosis_without_current_pathological_fracture', 'comorb_personal_history_of_malignant_neoplasm', 'comorb_gastro_esophageal_reflux_disease']]
concomitancy_details = master_data[['id', 'persistency_flag', 'concom_cholesterol_and_triglyceride_regulating_preparations', 'concom_narcotics', 'concom_systemic_corticosteroids_plain', 'concom_anti_depressants_and_mood_stabilisers', 'concom_fluoroquinolones', 'concom_cephalosporins', 'concom_macrolides_and_similar_types', 'concom_broad_spectrum_penicillins', 'concom_anaesthetics_general', 'concom_viral_vaccines']]
risk_factors = master_data[['id', 'persistency_flag', 'risk_type_1_insulin_dependent_diabetes', 'risk_osteogenesis_imperfecta', 'risk_rheumatoid_arthritis', 'risk_untreated_chronic_hyperthyroidism', 'risk_untreated_chronic_hypogonadism', 'risk_untreated_early_menopause', 'risk_patient_parent_fractured_their_hip', 'risk_smoking_tobacco', 'risk_chronic_malnutrition_or_malabsorption', 'risk_chronic_liver_disease', 'risk_family_history_of_osteoporosis', 'risk_low_calcium_intake', 'risk_vitamin_d_insufficiency', 'risk_poor_health_frailty', 'risk_excessive_thinness', 'risk_hysterectomy_oophorectomy', 'risk_estrogen_deficiency', 'risk_immobilization', 'risk_recurring_falls', 'count_of_risks']]

# calculate the count of 'Y' values for comorbidity details
master_data['comorb_count'] = comorbidity_details.iloc[:, 2:].apply(lambda row: row.eq('Y').sum(), axis=1)

# calculate the count of 'Y' values for concomitancy details
master_data['concom_count'] = concomitancy_details.iloc[:, 2:].apply(lambda row: row.eq('Y').sum(), axis=1)

# update dataframes with the counts
comorbidity_details = master_data[['id', 'persistency_flag', 'comorb_encounter_for_screening_for_malignant_neoplasms', 'comorb_encounter_for_immunization', 'comorb_encntr_for_general_exam_w_o_complaint,_susp_or_reprtd_dx', 'comorb_vitamin_d_deficiency', 'comorb_other_joint_disorder_not_elsewhere_classified', 'comorb_encntr_for_oth_sp_exam_w_o_complaint_suspected_or_reprtd_dx', 'comorb_long_term_current_drug_therapy', 'comorb_dorsalgia', 'comorb_personal_history_of_other_diseases_and_conditions', 'comorb_other_disorders_of_bone_density_and_structure', 'comorb_disorders_of_lipoprotein_metabolism_and_other_lipidemias', 'comorb_osteoporosis_without_current_pathological_fracture', 'comorb_personal_history_of_malignant_neoplasm', 'comorb_gastro_esophageal_reflux_disease', 'comorb_count']]
concomitancy_details = master_data[['id', 'persistency_flag', 'concom_cholesterol_and_triglyceride_regulating_preparations', 'concom_narcotics', 'concom_systemic_corticosteroids_plain', 'concom_anti_depressants_and_mood_stabilisers', 'concom_fluoroquinolones', 'concom_cephalosporins', 'concom_macrolides_and_similar_types', 'concom_broad_spectrum_penicillins', 'concom_anaesthetics_general', 'concom_viral_vaccines', 'concom_count']]

# create a dictionary of dataframes with their corresponding filenames
dataframes = {
    'dataset': master_data,
    'demographic_details': demographic_details,
    'provider_attributes': provider_attributes,
    'clinical_factors': clinical_factors,
    'comorbidity_details': comorbidity_details,
    'concomitancy_details': concomitancy_details,
    'risk_factors': risk_factors
}

# check if the 'datasets' folder exists, if not create it
if not os.path.exists('datasets'):
    os.makedirs('datasets')

# save each dataframe as a CSV file in the 'datasets' folder
for name, df in dataframes.items():
    filename = os.path.join('datasets', name + '.csv')
    df.to_csv(filename, index=False)
    print(f"Saved {filename} successfully. Shape: {df.shape}")