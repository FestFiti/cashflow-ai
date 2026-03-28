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
		renderer.toneMappingExposure = 1.8;
		container.appendChild(renderer.domElement);

		// ── LIGHTS ──
		scene.add(new THREE.AmbientLight(0xffffff, 0.54));

		// Big white fill from front-center
		const whiteFill = new THREE.PointLight(0xffffff, 6000, 60);
		whiteFill.position.set(0, 8, 14);
		scene.add(whiteFill);

		// Gold accent
		const goldA = new THREE.PointLight(0xffcc22, 520, 45);
		goldA.position.set(-2.5, 5.5, 6.5);
		scene.add(goldA);

		// Warm-orange fill
		const goldB = new THREE.PointLight(0xff8800, 140, 36);
		goldB.position.set(-6.5, 0.5, 5);
		scene.add(goldB);

		// Deep blue bottom-right
		const blue = new THREE.PointLight(0x1133ff, 340, 48);
		blue.position.set(3.5, -9.5, 2.5);
		scene.add(blue);

		// Cyan rim hint
		const cyan = new THREE.PointLight(0x00aaff, 60, 26);
		cyan.position.set(7, 0, 3);
		scene.add(cyan);

		// Back-rim directional
		const rim = new THREE.DirectionalLight(0x8899aa, 3.5);
		rim.position.set(0, 4, -7);
		scene.add(rim);

		// Violet accent
		const violet = new THREE.PointLight(0x6611bb, 55, 24);
		violet.position.set(2.5, 3.5, -4.5);
		scene.add(violet);

		// ── MATERIAL — dark liquid mercury / black chrome ──
		const mat = new THREE.MeshPhysicalMaterial({
			color: 0x060606,
			metalness: 1.0,
			roughness: 0.055,
			clearcoat: 1.0,
			clearcoatRoughness: 0.04,
			reflectivity: 1.0,
			envMapIntensity: 0.35,
		});

		// ── GEOMETRY — large sphere, pushed down to show dome ──
		const geo = new THREE.IcosahedronGeometry(5.5, 100);
		const blob = new THREE.Mesh(geo, mat);
		blob.position.set(0.2, -5.8, 0);
		scene.add(blob);

		// Store rest positions
		const posAttr = geo.getAttribute('position');
		const nV = posAttr.count;
		const rest: THREE.Vector3[] = [];
		for (let i = 0; i < nV; i++) {
			rest.push(new THREE.Vector3(posAttr.getX(i), posAttr.getY(i), posAttr.getZ(i)));
		}

		// ── Animation ──
		let t = 0;
		let raf: number;

		function tick() {
			raf = requestAnimationFrame(tick);
			t += 0.0018;

			const pos = geo.getAttribute('position');

			for (let i = 0; i < nV; i++) {
				const v = rest[i];

				// Low-frequency swell — silky smooth surface
				const n1 = noise3D(
					v.x * 0.14 + t,
					v.y * 0.14 + t * 0.65,
					v.z * 0.14
				);

				// Very faint second octave — barely perceptible texture
				const n2 = noise3D(
					v.x * 0.30 + t * 1.2,
					v.y * 0.30,
					v.z * 0.30 + t * 0.8
				);

				// Tiny amplitude = smooth liquid look
				const d = 1.0 + n1 * 0.09 + n2 * 0.025;
				pos.setXYZ(i, v.x * d, v.y * d, v.z * d);
			}

			pos.needsUpdate = true;
			geo.computeVertexNormals();

			blob.rotation.y -= 0.0007;
			blob.rotation.z += 0.00022;
			blob.position.y = -5.8 + Math.sin(t * 1.4) * 0.18;

			renderer.render(scene, camera);
		}
		tick();

		// ── Resize ──
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
