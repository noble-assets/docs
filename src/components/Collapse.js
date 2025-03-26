import React, { useState } from 'react';

const Collapse = ({ summary, children }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div style={{ marginBottom: '10px', border: '1px solid #ddd', borderRadius: '5px', padding: '10px' }}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          background: 'none',
          border: 'none',
          fontSize: '16px',
          fontWeight: 'bold',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center'
        }}
      >
        {isOpen ? '▼' : '▶'} <span dangerouslySetInnerHTML={{ __html: summary }} />
      </button>
      {isOpen && <div style={{ marginTop: '10px' }}>{children}</div>}
    </div>
  );
};

export default Collapse;
