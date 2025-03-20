
# without plotting xticks

plot_ash_model_results test/data/hysplit_operational.nc --model hysplit --output_dir tmp_hysplit_operational --verbose
plot_ash_model_results test/data/cdump_sum_Ruapehu_QVA_high.nc --model hysplit --output_dir tmp_cdump_sum_Ruapehu_QVA_high --verbose
plot_ash_model_results test/data/cdump_sum_Ruapehu_QVA_high.nc --model hysplit --output_dir tmp_cdump_sum_Ruapehu_QVA_high_limits180 --verbose --limits 165 -45 180 -32

:: only shows up to 180 anyway
plot_ash_model_results test/data/cdump_sum_Ruapehu_QVA_high.nc --model hysplit --output_dir tmp_cdump_sum_Ruapehu_QVA_high_limits190 --verbose --limits 165 -45 190 -32

:: it's plotting something for deposition??
plot_ash_model_results test/data/cdump_sum.nc --model hysplit --output_dir tmp_cdump_sum --verbose
plot_ash_model_results test/data/cdump_sum.nc --model hysplit --output_dir tmp_cdump_sum_limits --verbose --limits 165 -45 180 -32

# with ax.pcolormesh
clon = 0
plot_ash_model_results test/data/hysplit_operational.nc --model hysplit --output_dir tmp1_hysplit_operational --verbose

clon = 180
plot_ash_model_results test/data/cdump_sum_Ruapehu_QVA_high.nc --model hysplit --output_dir tmp1_cdump_sum_Ruapehu_QVA_high --verbose

# with ax.pcolormesh + ax.gridlines(draw_labels=True)

clon = 0
plot_ash_model_results test/data/hysplit_operational.nc --model hysplit --output_dir tmp2_hysplit_operational --verbose

clon = 180
plot_ash_model_results test/data/cdump_sum_Ruapehu_QVA_high.nc --model hysplit --output_dir tmp2_cdump_sum_Ruapehu_QVA_high --verbose


# with argument clon

plot_ash_model_results test/data/hysplit_operational.nc --model hysplit --output_dir tmp3_hysplit_operational --verbose --serial

plot_ash_model_results test/data/cdump_sum_Ruapehu_QVA_high.nc --model hysplit --output_dir tmp3_cdump_sum_Ruapehu_QVA_high --verbose --clon 180 --serial

:: has no deposition level
plot_ash_model_results test/data/cdump_sum.nc --model hysplit --output_dir tmp3_cdump_sum --verbose --clon 180 --serial
