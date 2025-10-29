"""
LeetCode Problem Search Tools

This module provides tools for finding LeetCode problems using AI knowledge.
"""

import re
from typing import Dict, Any
from google.adk.tools.tool_context import ToolContext


def search_leetcode_problem(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Find LeetCode problems using AI knowledge based on problem description or name.
    
    Uses built-in knowledge of popular LeetCode problems to generate URLs and basic info.
    """
    # Get the user's search query from tool context
    user_message = tool_context.state.get("user_message", "")
    
    if not user_message.strip():
        return {
            "status": "error",
            "message": "No search query provided. Please specify a LeetCode problem name or description."
        }
    
    # Use AI knowledge to find matching LeetCode problems
    search_query = user_message.lower().strip()
    
    # Common LeetCode problems mapping
    problem_mappings = {
        "two sum": ("two-sum", "1. Two Sum"),
        "add two numbers": ("add-two-numbers", "2. Add Two Numbers"),
        "longest substring": ("longest-substring-without-repeating-characters", "3. Longest Substring Without Repeating Characters"),
        "median two sorted arrays": ("median-of-two-sorted-arrays", "4. Median of Two Sorted Arrays"),
        "longest palindromic substring": ("longest-palindromic-substring", "5. Longest Palindromic Substring"),
        "reverse integer": ("reverse-integer", "7. Reverse Integer"),
        "palindrome number": ("palindrome-number", "9. Palindrome Number"),
        "container most water": ("container-with-most-water", "11. Container With Most Water"),
        "3sum": ("3sum", "15. 3Sum"),
        "valid parentheses": ("valid-parentheses", "20. Valid Parentheses"),
        "merge two sorted lists": ("merge-two-sorted-lists", "21. Merge Two Sorted Lists"),
        "remove duplicates": ("remove-duplicates-from-sorted-array", "26. Remove Duplicates from Sorted Array"),
        "maximum subarray": ("maximum-subarray", "53. Maximum Subarray"),
        "climbing stairs": ("climbing-stairs", "70. Climbing Stairs"),
        "merge sorted array": ("merge-sorted-array", "88. Merge Sorted Array"),
        "same tree": ("same-tree", "100. Same Tree"),
        "symmetric tree": ("symmetric-tree", "101. Symmetric Tree"),
        "maximum depth binary tree": ("maximum-depth-of-binary-tree", "104. Maximum Depth of Binary Tree"),
        "balanced binary tree": ("balanced-binary-tree", "110. Balanced Binary Tree"),
        "best time buy sell stock": ("best-time-to-buy-and-sell-stock", "121. Best Time to Buy and Sell Stock"),
        "valid palindrome": ("valid-palindrome", "125. Valid Palindrome"),
        "single number": ("single-number", "136. Single Number"),
        "linked list cycle": ("linked-list-cycle", "141. Linked List Cycle"),
        "majority element": ("majority-element", "169. Majority Element"),
        "reverse linked list": ("reverse-linked-list", "206. Reverse Linked List"),
        "contains duplicate": ("contains-duplicate", "217. Contains Duplicate"),
        "invert binary tree": ("invert-binary-tree", "226. Invert Binary Tree"),
        "valid anagram": ("valid-anagram", "242. Valid Anagram"),
        "missing number": ("missing-number", "268. Missing Number"),
        "move zeroes": ("move-zeroes", "283. Move Zeroes"),
    }
    
    # Try to find a direct match
    for pattern, (slug, title) in problem_mappings.items():
        if pattern in search_query or any(word in search_query for word in pattern.split()):
            url = f"https://leetcode.com/problems/{slug}/"
            return {
                "status": "success",
                "message": f"Found LeetCode problem: {title}",
                "data": {
                    "problem_url": url,
                    "problem_slug": slug,
                    "problem_title": title,
                    "search_query": user_message,
                    "match_type": "direct_mapping"
                }
            }
    
    # If no direct match, try to generate a slug from the search query
    potential_slug = re.sub(r'[^a-z0-9\s-]', '', search_query)
    potential_slug = re.sub(r'\s+', '-', potential_slug.strip())
    
    if potential_slug:
        url = f"https://leetcode.com/problems/{potential_slug}/"
        return {
            "status": "partial_success",
            "message": f"Generated potential LeetCode URL: {potential_slug}",
            "data": {
                "problem_url": url,
                "problem_slug": potential_slug,
                "search_query": user_message,
                "match_type": "generated_slug",
                "note": "This is a generated URL based on the search query. It may not exist on LeetCode."
            }
        }
    
    return {
        "status": "error",
        "message": f"Could not find or generate a LeetCode URL for query: '{user_message}'"
    }


def fallback_leetcode_search(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Fallback method when primary search fails.
    Provides suggestions for common LeetCode problem categories.
    """
    user_message = tool_context.state.get("user_message", "")
    
    if not user_message.strip():
        return {
            "status": "error",
            "message": "No search query available for fallback search."
        }
    
    search_query = user_message.lower().strip()
    
    # Category-based suggestions
    category_suggestions = {
        "array": ["two-sum", "maximum-subarray", "merge-sorted-array"],
        "string": ["valid-palindrome", "valid-anagram", "implement-strstr"],
        "linked list": ["reverse-linked-list", "merge-two-sorted-lists", "linked-list-cycle"],
        "tree": ["invert-binary-tree", "maximum-depth-of-binary-tree", "same-tree"],
        "dynamic programming": ["climbing-stairs", "best-time-to-buy-and-sell-stock"],
        "math": ["palindrome-number", "reverse-integer", "single-number"],
    }
    
    # Find relevant category
    for category, problems in category_suggestions.items():
        if category in search_query:
            first_problem = problems[0]
            url = f"https://leetcode.com/problems/{first_problem}/"
            return {
                "status": "success",
                "message": f"Found {category} problem suggestion: {first_problem}",
                "data": {
                    "problem_url": url,
                    "problem_slug": first_problem,
                    "search_query": user_message,
                    "match_type": "category_suggestion",
                    "category": category,
                    "other_suggestions": problems[1:]
                }
            }
    
    # Default fallback to Two Sum
    return {
        "status": "partial_success",
        "message": "Could not find specific match. Suggesting Two Sum as a starting problem.",
        "data": {
            "problem_url": "https://leetcode.com/problems/two-sum/",
            "problem_slug": "two-sum",
            "problem_title": "1. Two Sum",
            "search_query": user_message,
            "match_type": "default_fallback"
        }
    }