import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface AuthState {
	token: string | null;
	businessId: string | null;
	name: string | null;
	email: string | null;
}

const stored = browser ? localStorage.getItem('auth') : null;
const initial: AuthState = stored
	? JSON.parse(stored)
	: { token: null, businessId: null, name: null, email: null };

export const auth = writable<AuthState>(initial);

auth.subscribe((value) => {
	if (browser) {
		localStorage.setItem('auth', JSON.stringify(value));
		// Sync token to cookie for server-side auth guard
		if (value.token) {
			document.cookie = `auth_token=${value.token}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`;
		} else {
			document.cookie = 'auth_token=; path=/; max-age=0';
		}
	}
});

export function login(token: string, businessId: string, name: string, email?: string) {
	auth.set({ token, businessId, name, email: email ?? null });
}

export function logout() {
	auth.set({ token: null, businessId: null, name: null, email: null });
}
