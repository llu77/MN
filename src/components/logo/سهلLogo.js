
import React from 'react';
import './Logo.css';

const سهلLogo = ({ variant = 'header', className = '', ...props }) => {
  const variants = {
    header: { width: 180, height: 54, class: 'logo-header' },
    sidebar: { width: 150, height: 45, class: 'logo-sidebar' },
    footer: { width: 120, height: 36, class: 'logo-footer' },
    mobile: { width: 140, height: 42, class: 'logo-mobile' },
    print: { width: 200, height: 60, class: 'logo-print' }
  };

  const config = variants[variant] || variants.header;

  return (
    <img
      src="https://drive.google.com/file/d/1R3agKnUEBr9WMGrbiiJ0m7Pt92IYL9dq/view?usp=sharing"
      alt="سهل - نظام إدارة الصالونات متعددة الفروع"
      width={config.width}
      height={config.height}
      className={`logo ${config.class} ${className}`}
      {...props}
    />
  );
};

export default سهلLogo;
