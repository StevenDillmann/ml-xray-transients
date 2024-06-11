import os
import subprocess

def behr_hr(behr_directory, output_directory, soft_counts, hard_counts, soft_bkg, hard_bkg, area_ratio, conf='68.00'):
    
    # Round input values
    soft_counts = [round(i) for i in soft_counts]
    hard_counts = [round(i) for i in hard_counts]
    soft_bkg = [round(i) for i in soft_bkg]
    hard_bkg = [round(i) for i in hard_bkg]

    # Create output directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Run BEHR
    for i in range(0,len(soft_counts)):
        with open(output_directory + '/behr_out','w') as writeto:
            writeto.write(f'cd {behr_directory}')
            writeto.write(f'\n echo "softsrc={soft_counts[i]} hardsrc={hard_counts[i]}   softbkg={soft_bkg[i]}   hardbkg={hard_bkg[i]} softarea={area_ratio} hardarea={area_ratio} outputPr=True algo=quad"')
            writeto.write(f'\n./BEHR softsrc={soft_counts[i]} hardsrc={hard_counts[i]}   softbkg={soft_bkg[i]}   hardbkg={hard_bkg[i]} softarea={area_ratio} hardarea={area_ratio} output={output_directory}/bin{i} level={conf}')
        subprocess.run(f'bash {output_directory}/behr_out', shell = True)

    # Collect BEHR output
    medians = []
    uppers = []
    lowers = []
    for i in range(0,len(soft_counts)):
        med,upper,lower = behr_open(f'{output_directory}/bin{i}.txt')
        medians.append(med)
        uppers.append(upper)
        lowers.append(lower)

    # Create dictionary
    behr_result_out = {'hr': medians, 'hr_lo':lowers, 'hr_hi':uppers}
    return behr_result_out

def behr_open(file):
    with open(file,'r') as data:
        contents = data.read()
        line = contents.splitlines()[2].split()
        print("Option: ", line[0])
        med = line[3]
        lower = line[4]
        upper = line[5]

        # convert to float
        med = float(med)
        lower = float(lower)
        upper = float(upper)

    return med,upper,lower