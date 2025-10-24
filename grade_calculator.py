"""
Cambridge Grade Calculator Module
Handles score-to-grade conversion and weighted average calculations
"""

from config import GRADE_THRESHOLDS

class CambridgeGradeCalculator:
    """Calculator for Cambridge grading system"""
    
    def __init__(self):
        self.grade_thresholds = GRADE_THRESHOLDS
    
    def score_to_grade(self, score):
        """
        Convert a raw score (0-100) to Cambridge grade (A* to G)
        
        Args:
            score (float): Raw score between 0 and 100
            
        Returns:
            str: Cambridge grade (A*, A, B, C, D, E, F, G, or UNGRADED)
        """
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            return "UNGRADED"
        
        for threshold in self.grade_thresholds:
            if threshold["min"] <= score <= threshold["max"]:
                return threshold["grade"]
        
        return "UNGRADED"
    
    def calculate_weighted_average(self, scores_and_coefficients):
        """
        Calculate weighted average using Cambridge coefficient system
        
        Args:
            scores_and_coefficients (list): List of tuples (score, coefficient)
            
        Returns:
            float: Weighted average score
        """
        if not scores_and_coefficients:
            return 0.0
        
        weighted_sum = 0.0
        total_coefficient = 0.0
        
        for score, coefficient in scores_and_coefficients:
            if isinstance(score, (int, float)) and isinstance(coefficient, (int, float)):
                weighted_sum += score * coefficient
                total_coefficient += coefficient
        
        if total_coefficient == 0:
            return 0.0
        
        return weighted_sum / total_coefficient
    
    def calculate_final_grade(self, subject_data):
        """
        Calculate final weighted grade from multiple subjects
        
        Args:
            subject_data (list): List of dictionaries with keys: 'score', 'coefficient'
            
        Returns:
            dict: Dictionary with 'weighted_average' and 'final_grade'
        """
        scores_and_coefficients = [
            (data['score'], data['coefficient']) 
            for data in subject_data 
            if 'score' in data and 'coefficient' in data
        ]
        
        weighted_average = self.calculate_weighted_average(scores_and_coefficients)
        final_grade = self.score_to_grade(weighted_average)
        
        return {
            'weighted_average': round(weighted_average, 2),
            'final_grade': final_grade
        }
    
    def validate_score(self, score):
        """
        Validate if a score is within acceptable range
        
        Args:
            score: Score to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            score_float = float(score)
            return 0 <= score_float <= 100
        except (ValueError, TypeError):
            return False
    
    def get_grade_points(self, grade):
        """
        Convert Cambridge grade to numerical points for comparison
        
        Args:
            grade (str): Cambridge grade
            
        Returns:
            int: Grade points (8 for A*, 7 for A, etc.)
        """
        grade_points = {
            "A*": 8,
            "A": 7,
            "B": 6,
            "C": 5,
            "D": 4,
            "E": 3,
            "F": 2,
            "G": 1,
            "UNGRADED": 0
        }
        return grade_points.get(grade, 0)
    
    def generate_grade_breakdown(self, subject_data):
        """
        Generate detailed breakdown of grades and calculations
        
        Args:
            subject_data (list): List of subject data dictionaries
            
        Returns:
            dict: Detailed breakdown with individual grades and final calculation
        """
        breakdown = {
            "subjects": [],
            "total_weighted_score": 0.0,
            "total_coefficient": 0.0,
            "weighted_average": 0.0,
            "final_grade": "UNGRADED"
        }
        
        for data in subject_data:
            subject_grade = self.score_to_grade(data['score'])
            weighted_score = data['score'] * data['coefficient']
            
            subject_breakdown = {
                "name": data.get('name', 'Unknown'),
                "score": data['score'],
                "coefficient": data['coefficient'],
                "grade": subject_grade,
                "weighted_score": round(weighted_score, 2),
                "grade_points": self.get_grade_points(subject_grade)
            }
            
            breakdown["subjects"].append(subject_breakdown)
            breakdown["total_weighted_score"] += weighted_score
            breakdown["total_coefficient"] += data['coefficient']
        
        if breakdown["total_coefficient"] > 0:
            breakdown["weighted_average"] = round(
                breakdown["total_weighted_score"] / breakdown["total_coefficient"], 2
            )
            breakdown["final_grade"] = self.score_to_grade(breakdown["weighted_average"])
        
        return breakdown