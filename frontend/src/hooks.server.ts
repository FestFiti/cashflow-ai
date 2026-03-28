import type { Handle } from '@sveltejs/kit';

const PUBLIC_PATHS = ['/', '/login', '/register', '/forgot-password', '/reset-password'];

export const handle: Handle = async ({ event, resolve }) => {
	const path = event.url.pathname;

	// Allow public paths and static assets
	if (PUBLIC_PATHS.some((p) => path === p || path.startsWith(p + '/')) || path.startsWith('/_app')) {
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
