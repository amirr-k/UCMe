import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Logout = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    logout();
    const from = location.state?.from?.pathname || '/login';
    navigate(from, { replace: true });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '60vh' }}>
      <p>Signing you out...</p>
    </div>
  );
};

export default Logout; 