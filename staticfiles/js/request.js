document.addEventListener('DOMContentLoaded', function() {
    const verifyButton = document.getElementById('verify-account-btn');
    const accountNumberInput = document.getElementById('request_to');
    const recipientNameField = document.getElementById('recipient-name');
    const recipientDetails = document.getElementById('recipient-details');
    const accountError = document.getElementById('account-error');
    const accountSuccess = document.getElementById('account-success');
    
    // Check if all required elements exist
    if (!verifyButton || !accountNumberInput || !accountError || !accountSuccess) {
        console.error('Required elements not found');
        return;
    }
    
    function showError(message) {
        if (accountError) {
            accountError.textContent = message;
            accountError.style.display = 'block';
        }
        if (accountSuccess) {
            accountSuccess.style.display = 'none';
        }
        if (recipientDetails) {
            recipientDetails.style.display = 'none';
        }
        // Reset recipient fields
        if (recipientNameField) {
            recipientNameField.value = '';
        }
    }
    
    function showSuccess() {
        if (accountError) {
            accountError.style.display = 'none';
        }
        if (accountSuccess) {
            accountSuccess.style.display = 'block';
        }
        if (recipientDetails) {
            recipientDetails.style.display = 'block';
        }
    }
    
    function formatAccountNumber(number) {
        return number.replace(/(\d{4})/g, '$1 ').trim();
    }
    
    verifyButton.addEventListener('click', function(e) {
        e.preventDefault();
        
        const accountNumber = accountNumberInput.value.replace(/\s/g, '');
        if (!accountNumber) {
            showError('Please enter an account number');
            return;
        }
        
        // Show loading state
        verifyButton.disabled = true;
        verifyButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';
        
        fetch(`/bank-account/verify-account/${accountNumber}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update form fields with account data
                if (recipientNameField) {
                    recipientNameField.value = data.account_data.full_name;
                }
                if (accountNumberInput) {
                    accountNumberInput.value = formatAccountNumber(data.account_data.account_number);
                }
                showSuccess();
            } else {
                showError(data.message || 'Account not found');
            }
        })
        .catch(error => {
            showError('An error occurred while verifying the account');
            console.error('Error:', error);
        })
        .finally(() => {
            // Reset button state
            verifyButton.disabled = false;
            verifyButton.innerHTML = '<i class="fas fa-check-circle"></i> Verify Account';
        });
    });
    
    // Format account number as user types
    accountNumberInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\s/g, '');
        if (value.length > 16) {
            value = value.substr(0, 16);
        }
        e.target.value = formatAccountNumber(value);
    });
});
