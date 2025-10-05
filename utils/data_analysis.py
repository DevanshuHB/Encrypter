import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from collections import Counter

class DataAnalyzer:
    """
    Utility class for data analysis and visualization.
    Uses numpy, pandas, matplotlib, and seaborn.
    """

    def __init__(self):
        sns.set_style("whitegrid")

    def analyze_text_data(self, text_data):
        """
        Analyze text data and return statistics.
        """
        if not isinstance(text_data, str):
            text_data = str(text_data)

        # Basic statistics
        char_count = len(text_data)
        word_count = len(text_data.split())
        line_count = len(text_data.split('\n'))

        # Character frequency
        char_freq = Counter(text_data.lower())
        most_common_chars = char_freq.most_common(10)

        # Word frequency
        words = text_data.lower().split()
        word_freq = Counter(words)
        most_common_words = word_freq.most_common(10)

        return {
            'char_count': char_count,
            'word_count': word_count,
            'line_count': line_count,
            'most_common_chars': most_common_chars,
            'most_common_words': most_common_words
        }

    def create_character_frequency_plot(self, text_data):
        """
        Create a bar plot of character frequencies.
        Returns base64 encoded image.
        """
        if not isinstance(text_data, str):
            text_data = str(text_data)

        char_freq = Counter(text_data.lower())
        chars, counts = zip(*char_freq.most_common(20))

        plt.figure(figsize=(12, 6))
        plt.bar(chars, counts)
        plt.title('Character Frequency Analysis')
        plt.xlabel('Characters')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)

        # Convert plot to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()

        return image_base64

    def create_word_frequency_plot(self, text_data):
        """
        Create a bar plot of word frequencies.
        Returns base64 encoded image.
        """
        if not isinstance(text_data, str):
            text_data = str(text_data)

        words = text_data.lower().split()
        word_freq = Counter(words)
        words_list, counts = zip(*word_freq.most_common(20))

        plt.figure(figsize=(12, 6))
        plt.bar(words_list, counts)
        plt.title('Word Frequency Analysis')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')

        # Convert plot to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()

        return image_base64

    def analyze_numeric_data(self, data):
        """
        Analyze numeric data using numpy and pandas.
        """
        try:
            # Convert to numpy array
            if isinstance(data, str):
                # Try to parse as CSV-like data
                lines = data.strip().split('\n')
                numeric_data = []
                for line in lines:
                    try:
                        values = [float(x.strip()) for x in line.split(',')]
                        numeric_data.extend(values)
                    except ValueError:
                        continue
                arr = np.array(numeric_data)
            else:
                arr = np.array(data)

            if len(arr) == 0:
                return {'error': 'No numeric data found'}

            # Basic statistics
            stats = {
                'count': len(arr),
                'mean': np.mean(arr),
                'median': np.median(arr),
                'std': np.std(arr),
                'min': np.min(arr),
                'max': np.max(arr),
                'quartiles': np.percentile(arr, [25, 50, 75])
            }

            return stats

        except Exception as e:
            return {'error': f'Error analyzing numeric data: {str(e)}'}

    def create_histogram(self, data):
        """
        Create a histogram of numeric data.
        Returns base64 encoded image.
        """
        try:
            if isinstance(data, str):
                # Parse numeric data
                lines = data.strip().split('\n')
                numeric_data = []
                for line in lines:
                    try:
                        values = [float(x.strip()) for x in line.split(',')]
                        numeric_data.extend(values)
                    except ValueError:
                        continue
                arr = np.array(numeric_data)
            else:
                arr = np.array(data)

            if len(arr) == 0:
                return None

            plt.figure(figsize=(10, 6))
            plt.hist(arr, bins=30, edgecolor='black', alpha=0.7)
            plt.title('Data Distribution Histogram')
            plt.xlabel('Value')
            plt.ylabel('Frequency')

            # Convert plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()

            return image_base64

        except Exception as e:
            print(f"Error creating histogram: {e}")
            return None

def generate_pie_chart(score):
    """
    Generate a pie chart image as base64 string for the strength score.
    """
    labels = ['Strength', 'Weakness']
    sizes = [score, 100 - score]
    colors = ['#4CAF50', '#F44336']
    explode = (0.1, 0)  # explode the strength slice

    plt.figure(figsize=(4, 4))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64
