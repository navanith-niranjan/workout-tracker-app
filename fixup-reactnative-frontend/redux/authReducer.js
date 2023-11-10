import { createSlice } from '@reduxjs/toolkit';

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    isAuthenticated: false,
    user: null,
  },
  reducers: {
    setAuthState: (state, action) => {
      state.isAuthenticated = action.payload.isAuthenticated;
    },
    clearAuthState: (state) => {
      state.isAuthenticated = false;
      state.user = null;
    },
  },
});

export const { setAuthState , clearAuthState } = authSlice.actions;

export default authSlice.reducer;
