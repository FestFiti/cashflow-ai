import type { Handle } from '@sveltejs/kit';

const PUBLIC_PATHS = ['/', '/login', '/register', '/forgot-password', '/reset-password', '/pitch', '/demo', '/pay'];

export const handle: Handle = async ({ event, resolve }) => {
	const path = event.url.pathname;

	// Allow static assets (files with extensions), internal SvelteKit paths, and public routes
	if (
		path.includes('.') ||
		path.startsWith('/_app') ||
		PUBLIC_PATHS.some((p) => path === p || path.startsWith(p + '/'))
	) {
		return resolve(event);
	}

	// Check for auth token in cookie
	const token = event.cookies.get('auth_token');
	if (!token) {
		return new Response(null, {
			status: 302,
			headers: { Location: `/login?redirect=${encodeURIComponent(path)}` }
		});
	}

	event.locals.token = token;
	return resolve(event);
};
