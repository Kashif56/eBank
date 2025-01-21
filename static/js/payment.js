document.addEventListener('DOMContentLoaded', function() {
    const verifyButton = document.getElementById('verify-account-btn');
    const accountNumberInput = document.getElementById('account-number');
    const recipientNameField = document.getElementById('recipient-name');
    const accountTypeField = document.getElementById('account-type');
    const accountError = document.getElementById('account-error');
    const accountSuccess = document.getElementById('account-success');
    
    function showError(message) {
        accountError.textContent = message;
        accountError.style.display = 'block';
        accountSuccess.style.display = 'none';
        // Reset recipient fields
        recipientNameField.value = '';
        accountTypeField.value = '';
    }
    
    function showSuccess() {
        accountError.style.display = 'none';
        accountSuccess.style.display = 'block';
    }
    
    function formatAccountNumber(number) {
        return number.replace(/(\d{4})/g, '$1 ').trim();
    }
    
    if (verifyButton && accountNumberInput) {
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
                    recipientNameField.value = data.account_data.full_name;
                    accountTypeField.value = data.account_data.account_type;
                    accountNumberInput.value = formatAccountNumber(data.account_data.account_number);
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
    }
});
