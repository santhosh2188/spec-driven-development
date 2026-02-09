"""
Expense Tracker Application
A simple Flask-based expense tracking application with CRUD operations.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# In-memory data store
expenses = []
next_id = 1

CATEGORIES = [
    'Food & Dining',
    'Transportation',
    'Shopping',
    'Entertainment',
    'Bills & Utilities',
    'Healthcare',
    'Other'
]


class Expense:
    """Represents a single expense entry."""
    
    def __init__(self, amount, category, description, date=None, expense_id=None):
        global next_id
        self.id = expense_id if expense_id else next_id
        if not expense_id:
            next_id += 1
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')
    
    def to_dict(self):
        """Convert expense to dictionary."""
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date
        }


@app.route('/')
def index():
    """Display all expenses with optional filtering."""
    category_filter = request.args.get('category', '')
    
    filtered_expenses = expenses
    if category_filter:
        filtered_expenses = [e for e in expenses if e.category == category_filter]
    
    total = sum(e.amount for e in filtered_expenses)
    
    return render_template(
        'index.html',
        expenses=filtered_expenses,
        categories=CATEGORIES,
        selected_category=category_filter,
        total=total
    )


@app.route('/add', methods=['POST'])
def add_expense():
    """Add a new expense."""
    try:
        amount = request.form.get('amount')
        category = request.form.get('category')
        description = request.form.get('description')
        date = request.form.get('date')
        
        # Validation
        if not amount or not category or not description:
            flash('All fields are required!', 'error')
            return redirect(url_for('index'))
        
        if float(amount) <= 0:
            flash('Amount must be greater than zero!', 'error')
            return redirect(url_for('index'))
        
        expense = Expense(amount, category, description, date)
        expenses.append(expense)
        
        flash(f'Expense of ${expense.amount:.2f} added successfully!', 'success')
        return redirect(url_for('index'))
    
    except ValueError:
        flash('Invalid amount! Please enter a valid number.', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error adding expense: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    """Delete an expense by ID."""
    global expenses
    
    expense = next((e for e in expenses if e.id == expense_id), None)
    
    if expense:
        expenses[:] = [e for e in expenses if e.id != expense_id]  # Update in place
        flash(f'Expense deleted successfully!', 'success')
    else:
        flash('Expense not found!', 'error')
    
    return redirect(url_for('index'))


@app.route('/api/expenses', methods=['GET'])
def get_expenses_api():
    """API endpoint to get all expenses as JSON."""
    return jsonify([e.to_dict() for e in expenses])


@app.route('/api/summary', methods=['GET'])
def get_summary_api():
    """API endpoint to get expense summary by category."""
    summary = {}
    for expense in expenses:
        if expense.category in summary:
            summary[expense.category] += expense.amount
        else:
            summary[expense.category] = expense.amount
    
    total = sum(summary.values())
    
    return jsonify({
        'by_category': summary,
        'total': total,
        'count': len(expenses)
    })


@app.route('/clear', methods=['POST'])
def clear_expenses():
    """Clear all expenses (useful for testing)."""
    global expenses, next_id
    expenses[:] = []  # Clear in place instead of reassigning
    next_id = 1
    flash('All expenses cleared!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
