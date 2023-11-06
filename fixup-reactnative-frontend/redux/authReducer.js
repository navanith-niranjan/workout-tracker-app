import { createSlice } from '@reduxjs/toolkit';

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    isAuthenticated: false,
  },
  reducers: {
    setAuthState: (state, action) => {
      state.isAuthenticated = action.payload.isAuthenticated;
    },
  },
});

export const { setAuthState } = authSlice.actions;

export default authSlice.reducer;
