<script lang="ts">
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { createNoise3D } from 'simplex-noise';

	let container: HTMLDivElement;

	onMount(() => {
		const noise3D = createNoise3D();

		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 120);
		camera.position.set(0, 1.0, 12);

		const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
		renderer.setSize(container.clientWidth, container.clientHeight);
		renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
		renderer.toneMapping = THREE.ACESFilmicToneMapping;
		renderer.toneMappingExposure = 2.0;
		container.appendChild(renderer.domElement);

		// ── LIGHTS ──
		// Rich warm ambient — nothing is pure black
		scene.add(new THREE.AmbientLight(0xffeedd, 1.5));

		// Hemisphere — warm sky, cool ground = natural gradient across surface
		const hemi = new THREE.HemisphereLight(0xffd699, 0x1a2a5e, 2.2);
		scene.add(hemi);

		// Key — placed FAR away + very high intensity = wide soft falloff
		// This is the main highlight — far distance makes it spread across the surface
		const key = new THREE.PointLight(0xfff5e6, 18000, 100, 1.8);
		key.position.set(3, 16, 22);
		scene.add(key);

		// Warm fill — broad golden wash from left
		const fill = new THREE.PointLight(0xffaa33, 5000, 60, 1.8);
		fill.position.set(-14, 5, 12);
		scene.add(fill);

		// Back-rim — directional for wide even edge light
		const rimLight = new THREE.DirectionalLight(0xccddee, 4.0);
		rimLight.position.set(0, 6, -10);
		scene.add(rimLight);

		// Bottom blue — broad uplight
		const bottomBlue = new THREE.PointLight(0x2244cc, 3000, 60, 1.8);
		bottomBlue.position.set(3, -16, 8);
		scene.add(bottomBlue);

		// Cyan right rim — far away for broad highlight
		const cyanRim = new THREE.PointLight(0x44ccff, 1200, 50, 1.8);
		cyanRim.position.set(16, 2, 8);
		scene.add(cyanRim);

		// ── MATERIAL ──
		// roughness 0.28 = broad, soft, realistic specular spread
		// No clearcoat — it adds a sharp secondary highlight on top
		const mat = new THREE.MeshPhysicalMaterial({
			color: 0x141414,
			metalness: 1.0,
			roughness: 0.28,
			clearcoat: 0.0,
			reflectivity: 0.85,
			envMapIntensity: 0.3,
		});

		// ── GEOMETRY ──
		const geo = new THREE.IcosahedronGeometry(5.5, 48);
		const blob = new THREE.Mesh(geo, mat);
		blob.position.set(0.2, -5.8, 0);
		scene.add(blob);

		const posAttr = geo.getAttribute('position') as THREE.BufferAttribute;
		const nV = posAttr.count;
		const restX = new Float32Array(nV);
		const restY = new Float32Array(nV);
		const restZ = new Float32Array(nV);
		for (let i = 0; i < nV; i++) {
			restX[i] = posAttr.getX(i);
			restY[i] = posAttr.getY(i);
			restZ[i] = posAttr.getZ(i);
		}

		// ── Cursor ──
		let cursorX = 0, cursorY = 0;
		let smoothX = 0, smoothY = 0;
		const onMove = (e: MouseEvent) => {
			cursorX = (e.clientX / window.innerWidth - 0.5) * 2;
			cursorY = (e.clientY / window.innerHeight - 0.5) * 2;
		};
		window.addEventListener('mousemove', onMove, { passive: true });

		// ── Animation ──
		let t = 0;
		let raf: number;

		function tick() {
			raf = requestAnimationFrame(tick);
			t += 0.0016;

			smoothX += (cursorX - smoothX) * 0.03;
			smoothY += (cursorY - smoothY) * 0.03;

			const arr = posAttr.array as Float32Array;

			for (let i = 0; i < nV; i++) {
				const rx = restX[i];
				const ry = restY[i];
				const rz = restZ[i];

				// Very low frequency = massive smooth rolling hills and deep valleys
				const n = noise3D(
					rx * 0.06 + t,
					ry * 0.06 + t * 0.45,
					rz * 0.06
				);

				// amplitude 0.30 = deep valleys, tall peaks — very visible deformation
				const d = 1.0 + n * 0.30;

				const i3 = i * 3;
				arr[i3]     = rx * d;
				arr[i3 + 1] = ry * d;
				arr[i3 + 2] = rz * d;
			}

			posAttr.needsUpdate = true;
			geo.computeVertexNormals();

			blob.rotation.y = -t * 0.4 + smoothX * 0.3;
			blob.rotation.x = smoothY * 0.15;
			blob.rotation.z = Math.sin(t * 1.2) * 0.03;
			blob.position.y = -5.8 + Math.sin(t * 1.4) * 0.15;

			// Cursor shifts key light for dynamic highlight movement
			key.position.x = 3 + smoothX * 4;
			key.position.y = 16 + smoothY * 3;

			renderer.render(scene, camera);
		}
		tick();

		const onResize = () => {
			const w = container.clientWidth;
			const h = container.clientHeight;
			camera.aspect = w / h;
			camera.updateProjectionMatrix();
			renderer.setSize(w, h);
		};
		window.addEventListener('resize', onResize);

		return () => {
			cancelAnimationFrame(raf);
			window.removeEventListener('mousemove', onMove);
			window.removeEventListener('resize', onResize);
			renderer.dispose();
			geo.dispose();
			mat.dispose();
			if (container?.contains(renderer.domElement)) {
				container.removeChild(renderer.domElement);
			}
		};
	});
</script>

<div bind:this={container} class="absolute inset-0 z-0"></div>
