import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

def plot_waterfall(
    Xin_A, Xc_int_A, Xc_r_A, Xc_ext_A, X_ext_out_A, Xout_A,
    Xin_G, X_g, Xc_int_G, Xc_r_G, Xc_GHE, Xout_G,
):
    # Set up the subplots
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(dm.cm2in(16), dm.cm2in(5)), dpi=600)

    # Common settings
    bar_width = 0.4
    y_max = 6.8
    x_padding = 0.4
    annotation_size = dm.fs(-0.5)
    line_thickness = 0.1
    text_padding = 0.04

    # Function to draw connecting lines
    def draw_waterfall_lines(ax, x, cumulative_values, line_thickness):
        for i in range(1, len(x)):
            start = cumulative_values[i-1]
            end = cumulative_values[i]
            ax.plot([x[i-1]-bar_width/2, x[i]+bar_width/2], [start, start], color='dm.gray6', linestyle='-', linewidth=line_thickness)

    # ASHP plot
    labels_ashp = ['Input', r'$X_{c,int}$', r'$X_{c,ref}$', r'$X_{c,ext}$', r'$X_{ext,out}$', 'Output']
    values_ashp = [Xin_A, -Xc_int_A, -Xc_r_A, -Xc_ext_A, -X_ext_out_A, Xout_A]
    x_ashp = np.arange(len(labels_ashp))
    cumulative_values_ashp = np.cumsum(values_ashp)

    # Plot bars for ASHP
    for i in range(len(x_ashp)):
        if i == 0 or i == len(x_ashp) - 1:
            ax1.bar(x_ashp[i], values_ashp[i], bar_width, color='dm.indigo6')
        else:
            ax1.bar(x_ashp[i], values_ashp[i], bar_width, bottom=cumulative_values_ashp[i-1], color='dm.indigo6')

    # Draw connecting lines for ASHP
    draw_waterfall_lines(ax1, x_ashp, cumulative_values_ashp, line_thickness)

    # GSHP plot
    labels_gshp = ['Input', r'$X_{c,int}$', r'$X_{c,ref}$', r'$X_{c,GHE}$', 'Output']
    values_gshp = [Xin_G + X_g, -Xc_int_G, -Xc_r_G, -Xc_GHE, Xout_G]
    x_gshp = np.arange(len(labels_gshp))
    cumulative_values_gshp = np.cumsum(values_gshp)

    # Plot bars for GSHP
    for i in range(len(x_gshp)):
        if i == 0 or i == len(x_gshp) - 1:
            ax2.bar(x_gshp[i], values_gshp[i], bar_width, color='dm.lime6')
        else:
            ax2.bar(x_gshp[i], values_gshp[i], bar_width, bottom=cumulative_values_gshp[i-1], color='dm.lime6')

    # Draw connecting lines for GSHP
    draw_waterfall_lines(ax2, x_gshp, cumulative_values_gshp, line_thickness)

    # Common axis settings
    for ax in (ax1, ax2):
        ax.tick_params(axis='x', which='both', bottom=False, top=False)
        ax.tick_params(axis='y', which='both', left=True, right=False)
        ax.set_yticks([])
        ax.set_ylim(0, y_max)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(True)

    # Set x-axis labels and limits
    ax1.set_xticks(x_ashp)
    ax1.set_xticklabels(labels_ashp, ha='center', fontsize=dm.fs(0.3))
    ax1.set_xlim(-x_padding, len(labels_ashp) - 1 + x_padding)

    ax2.set_xticks(x_gshp)
    ax2.set_xticklabels(labels_gshp, ha='center', fontsize=dm.fs(0.3))
    ax2.set_xlim(-x_padding, len(labels_gshp) - 1 + x_padding)

    # Add bar values as text
    for ax, values, cumulative_values in [(ax1, values_ashp, cumulative_values_ashp), (ax2, values_gshp, cumulative_values_gshp)]:
        for i, value in enumerate(values):
            if i == 0 or i == len(values) - 1:
                height = value
                va = 'bottom'
                y_pos = height + text_padding
            else:
                height = cumulative_values[i]
                va = 'top'
                y_pos = height - text_padding
            
            sign = '-' if value < 0 else ''
            text_value = f'{abs(value):.1f}'
            
            # Combine sign and value, but add a small space between them
            full_text = f'{sign}{text_value}' if sign else text_value
            
            # Add the full text, centered on the bar
            ax.text(i, y_pos, full_text, ha='center', va=va, fontsize=dm.fs(0), weight='normal')

    # Create legend
    legend = fig.legend(
        [ax1.patches[0], ax2.patches[0]],
        ['ASHP', 'GSHP'],
        loc='upper right', ncol=2, frameon=False,
        fontsize=dm.fs(0.5), fancybox=False,
        columnspacing=1.05, labelspacing=0.8,
        bbox_to_anchor=(0.98, 0.98),
        handlelength=1.5
    )

    dm.simple_layout(fig, margins= (0.1,0.1,0.1,0.1) ,bbox = (0, 1, 0, 1), verbose=False)
    fig_name = 'exergy_distribution_comparison_waterfall_paper'
    # plt.savefig(save_dir + fig_name + '.png', dpi=600, transparent=True)
    # dm.util.save_and_show(fig, size=600)

    return fig