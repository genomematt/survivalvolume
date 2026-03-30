import unittest
import pandas as pd
import matplotlib.pyplot as plt

# Adjust imports based on your exact working directory / package setup
from survivalvolume.mresist import (
    calculate_mresist_gao,
    mresist_fisher_stats,
    check_normality_by_group,
    auto_run_mresist_stats,
    plot_mresist_waterfall
)
from survivalvolume.tests.test_data import test_data


class TestMResist(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the mRESIST results once for all tests to keep things fast."""
        cls.data = test_data
        cls.cutoff_day = 21
        cls.details_df, cls.summary_df = calculate_mresist_gao(cls.data, cutoff_day=cls.cutoff_day)

    def test_calculate_mresist_gao_structures(self):
        """Test that the Gao categorisation returns the correct DataFrame structures."""
        # Verify types
        self.assertIsInstance(self.details_df, pd.DataFrame)
        self.assertIsInstance(self.summary_df, pd.DataFrame)

        # Verify expected columns in details_df
        expected_details = ['Group', 'MouseID', 'Best_Response (%)', 'Day_of_Best', 'Best_Avg_Response (%)', 'mRESIST']
        for col in expected_details:
            self.assertIn(col, self.details_df.columns)

        # Verify expected columns in summary_df
        expected_summary = ['CR', 'PR', 'SD', 'PD', 'Censored']
        for col in expected_summary:
            self.assertIn(col, self.summary_df.columns)

    def test_cutoff_day_enforced(self):
        """Ensure the cutoff day is respected during calculations."""
        # Day of best response should never exceed the cutoff window
        self.assertTrue((self.details_df['Day_of_Best'] <= self.cutoff_day).all())

    def test_mresist_fisher_stats(self):
        """Test that Fisher's Exact Test executes and produces the expected comparisons."""
        stats_df = mresist_fisher_stats(self.summary_df)

        self.assertIsInstance(stats_df, pd.DataFrame)
        # 3 groups in test_data means 3 unique pairwise combinations
        self.assertEqual(len(stats_df), 3)
        self.assertIn('P_Raw', stats_df.columns)
        self.assertIn('P_Adj_FDR', stats_df.columns)

    def test_check_normality_by_group(self):
        """Test that the Shapiro-Wilk normality assessment runs smoothly."""
        normality_df, recommendation = check_normality_by_group(self.details_df)

        self.assertIsInstance(normality_df, pd.DataFrame)
        self.assertIn(recommendation, ["ANOVA", "Kruskal-Wallis"])
        self.assertIn('P_Shapiro', normality_df.columns)

    def test_auto_run_mresist_stats(self):
        """Test the automated statistical pipeline executes without crashing."""
        stats_result = auto_run_mresist_stats(self.details_df)

        self.assertIsInstance(stats_result, pd.DataFrame)
        self.assertIn('P_Value', stats_result.columns)

    def test_plot_mresist_waterfall(self):
        """Test that the plotting function handles the data and returns the plt module."""
        # Pass the plot to a variable and ensure it returns plt (as coded in mresist.py)
        plot_obj = plot_mresist_waterfall(self.details_df, title="Unit Test Waterfall")

        self.assertEqual(plot_obj, plt)

        # CRITICAL: Close the plot so it doesn't leave lingering figures in memory!
        plt.close('all')


if __name__ == '__main__':
    unittest.main()