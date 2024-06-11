import numpy as np

def rebinning(flare_counts, flare_time, soft_counts, hard_counts, soft_bkg, hard_bkg, min_counts_per_bin):
    delta_t = flare_time[1] - flare_time[0]
    new_counts = []
    new_time = []
    counts = 0
    times = []
    time_lo = []
    time_hi = []
    time_bins_counter = []
    hard_counts_counter = 0
    soft_counts_counter = 0
    soft_bkg_counter = 0
    hard_bkg_counter = 0
    soft_counts_new = []
    hard_counts_new = []
    soft_bkg_new = []
    hard_bkg_new = []
    counts_extra = []
    for i, c in enumerate(flare_counts):
        counts_extra.append(c)
        counts += c
        times.append(flare_time[i])
        hard_counts_counter += hard_counts[i]
        soft_counts_counter += soft_counts[i]
        soft_bkg_counter += soft_bkg[i]
        hard_bkg_counter += hard_bkg[i]
        if counts >= min_counts_per_bin:
            new_counts.append(counts)
            soft_counts_new.append(soft_counts_counter)
            hard_counts_new.append(hard_counts_counter)
            soft_bkg_new.append(soft_bkg_counter)
            hard_bkg_new.append(hard_bkg_counter)
            new_time.append(np.sum(np.array(times) * np.array(counts_extra)) / counts)
            time_lo.append(np.min(times)-delta_t )
            time_hi.append(np.max(times))
            time_bins_counter.append(len(times))
            counts = 0
            hard_counts_counter = 0
            soft_counts_counter = 0
            soft_bkg_counter = 0
            hard_bkg_counter = 0
            times = []
            counts_extra = []
    count_rate = np.array(new_counts) / (np.array(time_bins_counter) * delta_t)
    count_rate_error = np.sqrt(new_counts) / (np.array(time_bins_counter) * delta_t)

    # Create dictionary to store the new values
    output_lc_binned = {
        'counts': new_counts,
        'soft_counts': soft_counts_new,
        'hard_counts': hard_counts_new,
        'soft_bkg': soft_bkg_new,
        'hard_bkg': hard_bkg_new,
        'count_rate': count_rate,
        'count_rate_err': count_rate_error,
        'time': new_time,
        'time_lo': time_lo,
        'time_hi': time_hi
    }
    
    return output_lc_binned

def rebinning_strict(flare_counts, flare_time, soft_counts, hard_counts, soft_bkg, hard_bkg, strict_counts_per_bin):
    delta_t = flare_time[1] - flare_time[0]
    new_counts = []
    new_time = []
    time_lo = []
    time_hi = []
    
    soft_counts_new = []
    hard_counts_new = []
    soft_bkg_new = []
    hard_bkg_new = []
    
    temp_counts = 0
    temp_soft_counts = 0
    temp_hard_counts = 0
    temp_soft_bkg = 0
    temp_hard_bkg = 0
    temp_times = []
    
    for i in range(len(flare_counts)):
        temp_counts += flare_counts[i]
        temp_soft_counts += soft_counts[i]
        temp_hard_counts += hard_counts[i]
        temp_soft_bkg += soft_bkg[i]
        temp_hard_bkg += hard_bkg[i]
        temp_times.append(flare_time[i])
        
        if temp_counts >= strict_counts_per_bin:
            number_of_bins = int(temp_counts / strict_counts_per_bin)
            remaining_counts = temp_counts % strict_counts_per_bin
            bin_duration = (temp_times[-1] - temp_times[0]) / number_of_bins if number_of_bins > 0 else 0
            
            for j in range(number_of_bins):
                new_counts.append(strict_counts_per_bin)
                bin_start_time = temp_times[0] + j * bin_duration
                bin_end_time = bin_start_time + bin_duration
                
                new_time.append((bin_start_time + bin_end_time) / 2)
                time_lo.append(bin_start_time)
                time_hi.append(bin_end_time)
                
                count_ratio = strict_counts_per_bin / temp_counts
                soft_counts_new.append(temp_soft_counts * count_ratio)
                hard_counts_new.append(temp_hard_counts * count_ratio)
                soft_bkg_new.append(temp_soft_bkg * count_ratio)
                hard_bkg_new.append(temp_hard_bkg * count_ratio)
            
            # Update remaining counts and related data
            temp_counts = remaining_counts
            temp_soft_counts *= remaining_counts / temp_counts if temp_counts > 0 else 0
            temp_hard_counts *= remaining_counts / temp_counts if temp_counts > 0 else 0
            temp_soft_bkg *= remaining_counts / temp_counts if temp_counts > 0 else 0
            temp_hard_bkg *= remaining_counts / temp_counts if temp_counts > 0 else 0
            temp_times = [temp_times[-1]] if remaining_counts > 0 else []

    # Handle any leftover counts not forming a full bin
    if temp_counts > 0:
        new_counts.append(temp_counts)
        new_time.append(np.mean(temp_times))
        time_lo.append(temp_times[0] - delta_t / 2)
        time_hi.append(temp_times[-1] + delta_t / 2)
        
        soft_counts_new.append(temp_soft_counts)
        hard_counts_new.append(temp_hard_counts)
        soft_bkg_new.append(temp_soft_bkg)
        hard_bkg_new.append(temp_hard_bkg)

    count_rate = np.array(new_counts) / (np.array(time_hi) - np.array(time_lo))
    count_rate_error = np.sqrt(new_counts) / (np.array(time_hi) - np.array(time_lo))

    # Create dictionary to store the new values
    output_lc_binned = {
        'counts': new_counts,
        'soft_counts': soft_counts_new,
        'hard_counts': hard_counts_new,
        'soft_bkg': soft_bkg_new,
        'hard_bkg': hard_bkg_new,
        'count_rate': count_rate,
        'count_rate_err': count_rate_error,
        'time': new_time,
        'time_lo': time_lo,
        'time_hi': time_hi
    }
    
    return output_lc_binned


# def rebinning(flare_counts, flare_time, soft_counts, hard_counts, min_counts_per_bin):
#     delta_t = flare_time[1] - flare_time[0]
#     print('Delta t:', delta_t)
#     new_counts = []
#     new_time = []
#     counts = 0
#     times = []
#     time_bins_counter = []
#     hard_counts_counter = 0
#     soft_counts_counter = 0
#     soft_counts_new = []
#     hard_counts_new = []
#     for i, c in enumerate(flare_counts):
#         counts += c
#         times.append(flare_time[i])
#         hard_counts_counter += hard_counts[i]
#         soft_counts_counter += soft_counts[i]
#         if counts >= min_counts_per_bin:
#             new_counts.append(counts)
#             soft_counts_new.append(soft_counts_counter)
#             hard_counts_new.append(hard_counts_counter)
#             new_time.append(np.mean(times))
#             time_bins_counter.append(len(times))
#             counts = 0
#             hard_counts_counter = 0
#             soft_counts_counter = 0
#             times = []
#     count_rate = np.array(new_counts) / (np.array(time_bins_counter) * delta_t)
#     return new_counts, new_time, time_bins_counter, count_rate, soft_counts_new, hard_counts_new



def rebin_lightcurve(counts, bin_centers, bin_width, max_counts):
    # Calculate the time edges from the bin centers
    half_width = bin_width / 2
    bin_edges_lower = [center - half_width for center in bin_centers]
    bin_edges_upper = [center + half_width for center in bin_centers]

    # Initialize variables for the re-binning process
    new_bins = []
    new_bin_counts = 0
    new_bin_start = bin_edges_lower[0]

    # Iterate over each bin to accumulate counts and define new bins
    for i in range(len(counts)):
        if new_bin_counts + counts[i] > max_counts:
            # Finalize the current new bin
            new_bins.append({
                'count': new_bin_counts,
                'start_time': new_bin_start,
                'end_time': bin_edges_upper[i - 1]
            })
            # Start a new bin
            new_bin_counts = counts[i]
            new_bin_start = bin_edges_lower[i]
        else:
            # Add counts to the current new bin
            new_bin_counts += counts[i]

    # Add the last new bin if it has any counts
    if new_bin_counts > 0:
        new_bins.append({
            'count': new_bin_counts,
            'start_time': new_bin_start,
            'end_time': bin_edges_upper[-1]
        })

    return new_bins