import React, { forwardRef } from 'react';

export interface FormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

const FormInput = forwardRef<HTMLInputElement, FormInputProps>(
  ({ label, error, helperText, className = '', ...props }, ref) => {
    return (
      <div className="form-group">
        {label && (
          <label htmlFor={props.id} className="form-label">
            {label}
          </label>
        )}
        <input
          ref={ref}
          className={`form-input ${error ? 'border-error-500 focus:ring-error-500 focus:border-error-500' : ''} ${className}`}
          {...props}
        />
        {error && <p className="form-error">{error}</p>}
        {helperText && !error && <p className="mt-1 text-sm text-gray-500">{helperText}</p>}
      </div>
    );
  }
);

FormInput.displayName = 'FormInput';

export default FormInput;