"""
Log Analyzer Module

This module handles log analysis, counting, and frequency analysis.
It provides comprehensive log statistics and insights.
"""

from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional
from parser import LogParser


class LogAnalyzer:
    """
    A class for analyzing log data and generating statistics.
    
    Attributes:
        parser (LogParser): LogParser instance for reading log files
    """
    
    def __init__(self, parser: LogParser):
        """
        Initialize the LogAnalyzer with a LogParser instance.
        
        Args:
            parser (LogParser): LogParser instance for reading log files
        """
        self.parser = parser
        self.stats = {
            'total_entries': 0,
            'error_count': 0,
            'warning_count': 0,
            'info_count': 0,
            'debug_count': 0,
            'unknown_count': 0
        }
        self.error_messages = Counter()
        self.warning_messages = Counter()
        self.info_messages = Counter()
        self.hourly_distribution = defaultdict(int)
        self.daily_distribution = defaultdict(int)
    
    def analyze_logs(self) -> Dict:
        """
        Analyze the log file and generate comprehensive statistics.
        
        Returns:
            Dict: Complete analysis results
        """
        try:
            # Validate file first
            self.parser.validate_file()
            
            # Process each line
            for line in self.parser.read_lines():
                self._process_line(line)
            
            # Generate analysis results
            return self._generate_analysis_results()
            
        except Exception as e:
            raise Exception(f"Error during log analysis: {e}")
    
    def _process_line(self, line: str) -> None:
        """
        Process a single log line and update statistics.
        
        Args:
            line (str): A single line from the log file
        """
        if not line.strip():
            return
        
        # Parse the log entry
        log_entry = self.parser.parse_log_entry(line)
        if not log_entry:
            return
        
        # Update total count
        self.stats['total_entries'] += 1
        
        # Update level-specific counts
        level = log_entry['level']
        message = log_entry.get('message', '')
        
        if level == 'ERROR':
            self.stats['error_count'] += 1
            if message:
                # Count unique error messages (first 100 chars to avoid too specific errors)
                error_key = message[:100].strip()
                self.error_messages[error_key] += 1
                
        elif level == 'WARNING':
            self.stats['warning_count'] += 1
            if message:
                warning_key = message[:100].strip()
                self.warning_messages[warning_key] += 1
                
        elif level == 'INFO':
            self.stats['info_count'] += 1
            if message:
                info_key = message[:100].strip()
                self.info_messages[info_key] += 1
                
        elif level == 'DEBUG':
            self.stats['debug_count'] += 1
            
        else:
            self.stats['unknown_count'] += 1
    
    def _generate_analysis_results(self) -> Dict:
        """
        Generate comprehensive analysis results.
        
        Returns:
            Dict: Complete analysis results with statistics and insights
        """
        results = {
            'file_info': self.parser.get_file_info(),
            'statistics': self.stats.copy(),
            'level_percentages': self._calculate_percentages(),
            'most_frequent_errors': self._get_top_messages(self.error_messages, 5),
            'most_frequent_warnings': self._get_top_messages(self.warning_messages, 5),
            'most_frequent_info': self._get_top_messages(self.info_messages, 5),
            'error_rate': self._calculate_error_rate(),
            'health_score': self._calculate_health_score()
        }
        
        return results
    
    def _calculate_percentages(self) -> Dict[str, float]:
        """
        Calculate percentage distribution of log levels.
        
        Returns:
            Dict[str, float]: Percentage distribution of each log level
        """
        total = self.stats['total_entries']
        if total == 0:
            return {}
        
        percentages = {}
        for level, count in self.stats.items():
            if level != 'total_entries':
                percentages[level] = round((count / total) * 100, 2)
        
        return percentages
    
    def _get_top_messages(self, message_counter: Counter, top_n: int = 5) -> List[Tuple[str, int]]:
        """
        Get the most frequent messages from a counter.
        
        Args:
            message_counter (Counter): Counter containing message frequencies
            top_n (int): Number of top messages to return
            
        Returns:
            List[Tuple[str, int]]: List of (message, count) tuples
        """
        return message_counter.most_common(top_n)
    
    def _calculate_error_rate(self) -> float:
        """
        Calculate the error rate as a percentage.
        
        Returns:
            float: Error rate percentage
        """
        total = self.stats['total_entries']
        if total == 0:
            return 0.0
        
        return round((self.stats['error_count'] / total) * 100, 2)
    
    def _calculate_health_score(self) -> str:
        """
        Calculate a simple health score based on log distribution.
        
        Returns:
            str: Health score (EXCELLENT, GOOD, WARNING, CRITICAL)
        """
        error_rate = self._calculate_error_rate()
        
        if error_rate == 0:
            return "EXCELLENT"
        elif error_rate < 1:
            return "GOOD"
        elif error_rate < 5:
            return "WARNING"
        else:
            return "CRITICAL"
    
    def generate_summary_report(self, analysis_results: Dict) -> str:
        """
        Generate a human-readable summary report.
        
        Args:
            analysis_results (Dict): Results from analyze_logs method
            
        Returns:
            str: Formatted summary report
        """
        report = []
        report.append("=" * 60)
        report.append("LOG ANALYSIS SUMMARY REPORT")
        report.append("=" * 60)
        
        # File information
        file_info = analysis_results.get('file_info', {})
        report.append(f"\nFile: {file_info.get('path', 'N/A')}")
        report.append(f"Size: {file_info.get('size_mb', 0)} MB")
        report.append(f"Total Lines: {file_info.get('line_count', 0)}")
        
        # Statistics
        stats = analysis_results.get('statistics', {})
        report.append(f"\nLOG STATISTICS:")
        report.append(f"  Total Entries: {stats.get('total_entries', 0)}")
        report.append(f"  ERROR Entries: {stats.get('error_count', 0)}")
        report.append(f"  WARNING Entries: {stats.get('warning_count', 0)}")
        report.append(f"  INFO Entries: {stats.get('info_count', 0)}")
        report.append(f"  DEBUG Entries: {stats.get('debug_count', 0)}")
        report.append(f"  UNKNOWN Entries: {stats.get('unknown_count', 0)}")
        
        # Percentages
        percentages = analysis_results.get('level_percentages', {})
        if percentages:
            report.append(f"\nDISTRIBUTION PERCENTAGES:")
            for level, percentage in percentages.items():
                report.append(f"  {level.capitalize()}: {percentage}%")
        
        # Health metrics
        report.append(f"\nHEALTH METRICS:")
        report.append(f"  Error Rate: {analysis_results.get('error_rate', 0)}%")
        report.append(f"  Health Score: {analysis_results.get('health_score', 'UNKNOWN')}")
        
        # Most frequent errors
        top_errors = analysis_results.get('most_frequent_errors', [])
        if top_errors:
            report.append(f"\nTOP ERROR MESSAGES:")
            for i, (message, count) in enumerate(top_errors, 1):
                # Truncate long messages for display
                display_message = message[:80] + "..." if len(message) > 80 else message
                report.append(f"  {i}. ({count} occurrences) {display_message}")
        
        # Most frequent warnings
        top_warnings = analysis_results.get('most_frequent_warnings', [])
        if top_warnings:
            report.append(f"\nTOP WARNING MESSAGES:")
            for i, (message, count) in enumerate(top_warnings, 1):
                display_message = message[:80] + "..." if len(message) > 80 else message
                report.append(f"  {i}. ({count} occurrences) {display_message}")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
    
    def export_to_dict(self, analysis_results: Dict) -> Dict:
        """
        Export analysis results to a clean dictionary format.
        
        Args:
            analysis_results (Dict): Results from analyze_logs method
            
        Returns:
            Dict: Clean dictionary format for export
        """
        export_data = {
            'analysis_timestamp': self._get_timestamp(),
            'file_information': analysis_results.get('file_info', {}),
            'log_statistics': analysis_results.get('statistics', {}),
            'level_distribution_percentages': analysis_results.get('level_percentages', {}),
            'health_metrics': {
                'error_rate': analysis_results.get('error_rate', 0),
                'health_score': analysis_results.get('health_score', 'UNKNOWN')
            },
            'top_errors': [
                {'message': msg, 'count': count} 
                for msg, count in analysis_results.get('most_frequent_errors', [])
            ],
            'top_warnings': [
                {'message': msg, 'count': count} 
                for msg, count in analysis_results.get('most_frequent_warnings', [])
            ]
        }
        
        return export_data
    
    def _get_timestamp(self) -> str:
        """
        Get current timestamp for export purposes.
        
        Returns:
            str: Current timestamp in ISO format
        """
        from datetime import datetime
        return datetime.now().isoformat()
