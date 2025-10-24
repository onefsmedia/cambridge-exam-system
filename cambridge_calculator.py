#!/usr/bin/env python3
"""
Cambridge Calculator Module
Handles grade calculations, coefficient modifications, and auto-grading
"""

class CambridgeCalculator:
    def __init__(self):
        # Cambridge grading scale
        self.grade_boundaries = {
            'A*': 90,
            'A': 80,
            'B': 70,
            'C': 60,
            'D': 50,
            'E': 40,
            'F': 30,
            'G': 20
        }
    
    def calculate_grade_from_score(self, score):
        """Calculate letter grade from numerical score"""
        if score >= 90:
            return 'A*'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        elif score >= 40:
            return 'E'
        elif score >= 30:
            return 'F'
        elif score >= 20:
            return 'G'
        else:
            return 'U'  # Ungraded
    
    def calculate_weighted_score(self, score, coefficient):
        """Calculate weighted score using coefficient"""
        return score * coefficient
    
    def calculate_results(self, grades_data):
        """
        Calculate comprehensive results
        grades_data should be: {subject_code: {'score': score, 'coefficient': coeff}}
        """
        total_weighted_score = 0
        total_coefficients = 0
        subject_results = {}
        
        for subject_code, data in grades_data.items():
            score = data['score']
            coefficient = data['coefficient']
            
            # Calculate weighted score
            weighted_score = self.calculate_weighted_score(score, coefficient)
            
            # Calculate grade
            grade = self.calculate_grade_from_score(score)
            
            subject_results[subject_code] = {
                'score': score,
                'weighted_score': weighted_score,
                'grade': grade,
                'coefficient': coefficient
            }
            
            total_weighted_score += weighted_score
            total_coefficients += coefficient
        
        # Calculate overall average
        overall_average = total_weighted_score / total_coefficients if total_coefficients > 0 else 0
        overall_grade = self.calculate_grade_from_score(overall_average)
        
        return {
            'subject_results': subject_results,
            'total_weighted_score': total_weighted_score,
            'total_coefficients': total_coefficients,
            'overall_average': overall_average,
            'overall_grade': overall_grade,
            'total_subjects': len(grades_data)
        }