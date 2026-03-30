import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests
from itertools import combinations
from matplotlib.patches import Patch
from scipy.stats import f_oneway, kruskal, shapiro


def calculate_mresist_gao(data_dict, cutoff_day=21):
    """
    Categorizes mouse tumor data using mRESIST criteria (Gao et al., 2015).

    The 'Best Average Response' is defined as the minimum value of the
    running average of percentage changes from Day 0 (V0) for each mouse.

    Parameters:
    - data_dict: Dict of DataFrames (keys=group names, columns=MouseIDs, index=Days)
    - cutoff_day: The day to stop the analysis (e.g., 21 or 28)

    Returns:
    - details_df: Per-mouse statistics including Best Avg Response and Category.
    - summary_df: Counts of each mRESIST category per treatment group.
    """
    all_mouse_stats = []

    for group_name, df in data_dict.items():
        # Ensure index is numeric and filter for the window
        df.index = pd.to_numeric(df.index)
        df_window = df[df.index <= cutoff_day]

        for mouse_id in df.columns:
            # 1. Prepare data and identify V0
            series = df_window[mouse_id].dropna()
            full_series = df[mouse_id].dropna()

            if series.empty:
                continue

            v0 = series.iloc[0]

            # 2. Check for Censoring (stops before the study cutoff)
            is_censored = False
            if not full_series.empty:
                if full_series.index[-1] < cutoff_day:
                    is_censored = True

            # 3. Calculate % Change from Baseline for every day
            pct_changes = ((series - v0) / v0) * 100

            # 4. Calculate Best Response (the single lowest % change)
            best_resp = pct_changes.min()
            day_of_best = pct_changes.idxmin()

            # 5. Calculate BEST AVERAGE RESPONSE (The Gao et al. metric)
            # We take the cumulative mean at each day, then find the minimum of those means
            running_averages = pct_changes.expanding().mean()
            best_avg_resp = running_averages.min()

            # 6. Apply mRESIST Logic
            if is_censored:
                status = 'Censored'
            elif best_resp <= -95 and best_avg_resp <= -40:
                status = 'CR'
            elif best_resp <= -50 and best_avg_resp <= -20:
                status = 'PR'
            elif best_resp <= 35 and best_avg_resp <= 30:
                status = 'SD'
            else:
                status = 'PD'

            all_mouse_stats.append({
                'Group': group_name,
                'MouseID': mouse_id,
                'Best_Response (%)': round(best_resp, 2),
                'Day_of_Best': day_of_best,
                'Best_Avg_Response (%)': round(best_avg_resp, 2),
                'mRESIST': status
            })

    details_df = pd.DataFrame(all_mouse_stats)

    # Generate Summary Table
    summary = details_df.groupby(['Group', 'mRESIST']).size().unstack(fill_value=0)

    # Ensure all standard columns are present
    cols = ['CR', 'PR', 'SD', 'PD', 'Censored']
    for col in cols:
        if col not in summary.columns:
            summary[col] = 0

    return details_df, summary[cols]


def mresist_fisher_stats(summary_df):
    """
    Performs pairwise Fisher's Exact Tests on Responder (CR+PR+SD) vs.
    Non-Responder (PD) counts and applies Benjamini-Hochberg correction.
    """
    comparisons = []
    p_values = []

    # 1. Generate Pairwise Comparisons
    groups = summary_df.index.tolist()
    for g1, g2 in combinations(groups, 2):
        # Counts for Group 1
        r1 = summary_df.loc[g1, ['CR', 'PR', 'SD']].sum()
        nr1 = summary_df.loc[g1, 'PD']

        # Counts for Group 2
        r2 = summary_df.loc[g2, ['CR', 'PR', 'SD']].sum()
        nr2 = summary_df.loc[g2, 'PD']

        # Build 2x2 table: [[Resp_G1, NonResp_G1], [Resp_G2, NonResp_G2]]
        table = [[r1, nr1], [r2, nr2]]
        _, p_val = fisher_exact(table)

        comparisons.append({
            'Comparison': f"{g1} vs {g2}",
            'G1_Rate': f"{int(r1)}/{int(r1 + nr1)}",
            'G2_Rate': f"{int(r2)}/{int(r2 + nr2)}",
            'P_Raw': p_val
        })
        p_values.append(p_val)

    # 2. Apply Benjamini-Hochberg (FDR) Correction
    # 'fdr_bh' is standard for discovery; use 'bonferroni' for stricter control
    if p_values:
        _, p_corrected, _, _ = multipletests(p_values, method='fdr_bh')

        # Update results with corrected values
        for i, result in enumerate(comparisons):
            result['P_Adj_FDR'] = p_corrected[i]
            result['Significant'] = p_corrected[i] < 0.05

    return pd.DataFrame(comparisons)


def plot_mresist_waterfall(details_df, colors=None, show_labels=True, title="mRESIST Waterfall Plot"):
    """
    Plots a waterfall chart of Best Average Response.
    Supports any number of groups with automatic color assignment.
    """
    # 1. Filter out Censored mice
    plot_df = details_df[details_df['mRESIST'] != 'Censored'].copy()

    # 2. Sort by Best Average Response descending
    plot_df = plot_df.sort_values('Best_Avg_Response (%)', ascending=False)

    # 3. Handle Colors (Custom or Automatic)
    if colors is None:
        unique_groups = sorted(plot_df['Group'].unique())
        cmap = plt.get_cmap('tab10')
        colors = {group: cmap(i % 10) for i, group in enumerate(unique_groups)}

    plot_df['color'] = plot_df['Group'].map(colors)

    # 4. Create the plot
    plt.figure(figsize=(14, 7))
    bars = plt.bar(plot_df['MouseID'], plot_df['Best_Avg_Response (%)'],
                   color=plot_df['color'], edgecolor='black', alpha=0.85)

    # 5. Add mRESIST labels
    if show_labels:
        for bar, label in zip(bars, plot_df['mRESIST']):
            yval = bar.get_height()
            va = 'bottom' if yval >= 0 else 'top'
            offset = 1.5 if yval >= 0 else -1.5
            plt.text(bar.get_x() + bar.get_width() / 2, yval + offset,
                     label, ha='center', va=va, fontsize=8, fontweight='bold')

    # 6. Reference lines
    plt.axhline(y=30, color='#c0392b', linestyle='--', linewidth=1.2, label='SD Threshold (+30%)')
    plt.axhline(y=0, color='black', linewidth=1)

    # 7. Formatting
    plt.title(title, fontsize=14, fontweight='bold', pad=25)
    plt.ylabel('Best Average Response (%)', fontsize=11)
    plt.xlabel('Individual Mouse ID', fontsize=11)
    plt.xticks(rotation=45, ha='right')

    # Adjust Y-axis to prevent label clipping
    ymin, ymax = plt.ylim()
    plt.ylim(ymin * 1.15 if ymin < 0 else -10, ymax * 1.15)

    # 8. Legend - Dynamically built from groups present in the data
    legend_elements = [Patch(facecolor=colors[g], edgecolor='black',
                             label=str(g).replace('_', ' ').title())
                       for g in colors if g in plot_df['Group'].unique()]

    legend_elements.append(plt.Line2D([0],[0], color = '#c0392b', linestyle = '--', label = 'SD Cutoff'))
    plt.legend(handles=legend_elements, loc='upper right', frameon=True, fontsize=10)

    plt.tight_layout()
    return plt


def check_normality_by_group(details_df):
    """
    Performs Shapiro-Wilk test on 'Best_Avg_Response (%)' for each group.
    Returns a summary and a recommendation for which test to use.
    """
    # Exclude censored mice
    df = details_df[details_df['mRESIST'] != 'Censored']
    results = []
    all_normal = True

    for group_name, group_data in df.groupby('Group'):
        values = group_data['Best_Avg_Response (%)'].values

        # Shapiro-Wilk requires at least 3 data points
        if len(values) < 3:
            results.append({
                'Group': group_name,
                'N': len(values),
                'P_Shapiro': np.nan,
                'Status': 'Insufficient Data (N<3)'
            })
            continue

        stat, p_val = shapiro(values)
        is_normal = p_val > 0.05
        if not is_normal: all_normal = False

        results.append({
            'Group': group_name,
            'N': len(values),
            'P_Shapiro': round(p_val, 4),
            'Status': 'Normal' if is_normal else 'Non-Normal'
        })

    recommendation = "ANOVA" if all_normal else "Kruskal-Wallis"
    return pd.DataFrame(results), recommendation


def auto_run_mresist_stats(details_df):
    """
    Automated pipeline: Checks normality and runs the appropriate
    statistical test (ANOVA or Kruskal-Wallis).
    """
    normality_df, test_type = check_normality_by_group(details_df)

    print(f"Normality Check Summary:\n{normality_df}\n")
    print(f"Recommended Test: {test_type}\n")

    if test_type == "ANOVA":
        return stats_anova_continuous(details_df)
    else:
        return stats_kruskal_nonparametric(details_df)


def stats_anova_continuous(details_df):
    """One-way ANOVA on Best Average Response across all groups."""
    df = details_df[details_df['mRESIST'] != 'Censored']

    # Group the continuous values into lists
    group_data = [group['Best_Avg_Response (%)'].values
                  for name, group in df.groupby('Group')]

    # Only run if we have at least 2 groups with data
    if len(group_data) < 2: return "Insufficient groups for ANOVA"

    f_stat, p_val = f_oneway(*group_data)
    return pd.DataFrame([{'Test': 'One-Way ANOVA', 'F_Stat': f_stat, 'P_Value': p_val}])

def stats_kruskal_nonparametric(details_df):
    """Kruskal-Wallis H-test for non-normal continuous data."""
    df = details_df[details_df['mRESIST'] != 'Censored']
    group_data = [group['Best_Avg_Response (%)'].values
                  for name, group in df.groupby('Group')]

    if len(group_data) < 2: return "Insufficient groups for Kruskal-Wallis"

    h_stat, p_val = kruskal(*group_data)
    return pd.DataFrame([{'Test': 'Kruskal-Wallis', 'H_Stat': h_stat, 'P_Value': p_val}])

