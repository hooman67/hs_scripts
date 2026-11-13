#!/usr/bin/env python3
"""
Census Demographic Diversity Calculator
Computes Simpson Diversity Index (Gini-Simpson) and related metrics
from Census Bureau ACS demographic breakdowns.
"""

import sys
from typing import Dict, Tuple

class DiversityCalculator:
    """Calculate demographic diversity indices from Census data."""
    
    def __init__(self):
        self.results = {}
    
    def calculate_indices(self, demographics: Dict[str, float]) -> Dict:
        """
        Calculate Simpson DI, HHI, and normalized scores.
        
        Args:
            demographics: Dict with category names, percentages (0-100)
                         e.g., {"White": 42.5, "Hispanic": 28.3, "Asian": 11.2, ...}
        
        Returns:
            Dict with all calculated indices and interpretations
        """
        # Convert percentages to proportions
        total = sum(demographics.values())
        if abs(total - 100.0) > 0.5:
            raise ValueError(f"Demographics don't sum to ~100%: {total:.1f}%")
        
        proportions = {k: v/100.0 for k, v in demographics.items()}
        
        # Calculate sum of squared proportions (HHI)
        sum_squares = sum(p**2 for p in proportions.values())
        
        # Simpson Diversity Index
        simpson_di = 1 - sum_squares
        
        # HHI (Herfindahl-Hirschman Index)
        hhi = sum_squares
        hhi_10000 = sum_squares * 10000
        
        # Maximum possible diversity for n categories
        n_categories = len(demographics)
        max_di = (n_categories - 1) / n_categories if n_categories > 1 else 0
        
        # Normalized diversity (percentage of maximum)
        normalized_di = (simpson_di / max_di * 100) if max_di > 0 else 0
        
        # Non-white percentage calculation
        white_pct = demographics.get("White (Non-Hispanic)", 0)
        non_white_pct = 100 - white_pct
        
        return {
            'total_categories': n_categories,
            'total_percentage': total,
            'demographics': demographics,
            'proportions': proportions,
            'simpson_di': simpson_di,
            'simpson_di_percent': simpson_di * 100,
            'normalized_di_percent': normalized_di,
            'hhi': hhi,
            'hhi_10000_scale': hhi_10000,
            'max_possible_di': max_di,
            'non_white_percentage': non_white_pct,
            'diversity_interpretation': self._interpret_diversity(simpson_di),
        }
    
    @staticmethod
    def _interpret_diversity(di: float) -> str:
        """Interpret Simpson DI on standard scale."""
        if di < 0.30:
            return "Low diversity (homogeneous)"
        elif di < 0.60:
            return "Moderate diversity"
        elif di < 0.80:
            return "High diversity"
        else:
            return "Very high diversity (heterogeneous)"
    
    def format_report(self, county_name: str, data: Dict, acs_year: str = "2023") -> str:
        """Format results as readable report."""
        output = []
        output.append("=" * 70)
        output.append(f"DEMOGRAPHIC DIVERSITY ANALYSIS: {county_name}")
        output.append("=" * 70)
        output.append(f"Data Source: ACS {acs_year} Estimates")
        output.append("")
        
        output.append("DEMOGRAPHIC BREAKDOWN:")
        output.append("-" * 70)
        for category, pct in sorted(data['demographics'].items(), key=lambda x: -x[1]):
            output.append(f"  {category:<40} {pct:6.2f}%")
        output.append("-" * 70)
        output.append(f"  {'Total':<40} {data['total_percentage']:6.2f}%")
        output.append(f"  {'Non-White Population':<40} {data['non_white_percentage']:6.2f}%")
        output.append("")
        
        output.append("DIVERSITY INDICES:")
        output.append("-" * 70)
        output.append(f"  Simpson Diversity Index (DI):        {data['simpson_di']:.4f}")
        output.append(f"  Simpson DI (as %)                    {data['simpson_di_percent']:.2f}%")
        output.append(f"  Normalized DI (% of max):            {data['normalized_di_percent']:.1f}%")
        output.append(f"  Interpretation:                      {data['diversity_interpretation']}")
        output.append(f"  Herfindahl-Hirschman Index (HHI):    {data['hhi']:.4f}")
        output.append(f"  HHI (0-10000 scale):                 {data['hhi_10000_scale']:.1f}")
        output.append("")
        
        output.append("DIVERSITY INTERPRETATION:")
        output.append("-" * 70)
        di = data['simpson_di']
        output.append(f"  • Probability two random residents")
        output.append(f"    are from different groups:        {di*100:.1f}%")
        output.append(f"  • Categories analyzed:               {data['total_categories']}")
        output.append(f"  • Maximum possible DI for {data['total_categories']} groups:     {data['max_possible_di']:.4f}")
        output.append(f"  • Relative to maximum:               {data['normalized_di_percent']:.1f}%")
        output.append("")
        
        return "\n".join(output)

def main():
    """Example usage with sample data."""
    calc = DiversityCalculator()
    
    # Sample data (illustrative - replace with actual Census data)
    # Adjusted to sum to 100%
    santa_cruz_data = {
        "White (Non-Hispanic)": 42.5,
        "Hispanic/Latino": 28.3,
        "Asian": 11.2,
        "Black/African American": 1.8,
        "Two or More Races": 3.9,
        "Native American/Alaska Native": 0.8,
        "Native Hawaiian/Pacific Islander": 0.7,
        "Other": 10.8,
    }
    
    monterey_data = {
        "White (Non-Hispanic)": 38.2,
        "Hispanic/Latino": 39.5,
        "Asian": 6.8,
        "Black/African American": 1.4,
        "Two or More Races": 3.2,
        "Native American/Alaska Native": 0.6,
        "Native Hawaiian/Pacific Islander": 0.3,
        "Other": 10.0,
    }
    
    # Calculate
    santa_cruz_results = calc.calculate_indices(santa_cruz_data)
    monterey_results = calc.calculate_indices(monterey_data)
    
    # Report
    print(calc.format_report("Santa Cruz County, CA", santa_cruz_results))
    print()
    print(calc.format_report("Monterey County, CA", monterey_results))
    
    # Comparison
    print()
    print("=" * 70)
    print("COUNTY COMPARISON")
    print("=" * 70)
    print(f"{'County':<30} {'Simpson DI':<15} {'Non-White %':<15}")
    print("-" * 70)
    print(f"{'Santa Cruz':<30} {santa_cruz_results['simpson_di']:.4f}         {santa_cruz_results['non_white_percentage']:6.2f}%")
    print(f"{'Monterey':<30} {monterey_results['simpson_di']:.4f}         {monterey_results['non_white_percentage']:6.2f}%")
    print()

if __name__ == "__main__":
    main()

