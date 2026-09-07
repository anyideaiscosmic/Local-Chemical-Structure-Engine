import initIndigo from 'indigo-ketcher';

let indigo = null;
let renderer = null;

// --- 1. Initialize Indigo WASM ---
async function init() {
    const module = await initIndigo();
    indigo = module.indigo;
    renderer = module.indigoRenderer;
    // Set rendering options (margins, etc.)
    indigo.setOption('render-margins', 20, 20);
    indigo.setOption('render-output-format', 'svg');
    document.getElementById('status').textContent = '✅ Indigo loaded. Ready!';
}

// --- 2. Core function: Name → 3D Structure → SVG ---
function generateStructure(name) {
    if (!indigo) {
        throw new Error('Indigo not initialized yet.');
    }

    // Step A: Parse IUPAC name to molecule
    // Indigo's nameToStructure handles systematic IUPAC names directly[reference:2]
    const mol = indigo.nameToStructure(name);

    // Step B: Generate 3D coordinates
    // (Indigo's layout() gives 2D; for 3D we use the 3D generation method)
    // The exact 3D generation API may vary; check indigo-ketcher docs.
    // A common approach: use mol.layout() for 2D, then use a force-field.
    // For now, we'll use the built-in layout (2D) and later upgrade to 3D.
    mol.layout();  // Generates 2D coordinates

    // Step C: Render to SVG
    // renderer.renderToBuffer() returns the image data[reference:3]
    const svgData = renderer.renderToBuffer(mol);

    // Step D: Convert to a usable SVG string
    const svgString = new TextDecoder().decode(svgData);

    return svgString;
}

// --- 3. Handle user interaction ---
document.getElementById('generateBtn').addEventListener('click', async () => {
    const nameInput = document.getElementById('nameInput');
    const status = document.getElementById('status');
    const container = document.getElementById('svg-container');

    const name = nameInput.value.trim();
    if (!name) {
        status.textContent = '⚠️ Please enter a chemical name.';
        return;
    }

    status.textContent = `⏳ Processing "${name}"...`;

    try {
        const svg = generateStructure(name);
        container.innerHTML = svg;  // Insert the SVG directly
        status.textContent = `✅ Generated structure for "${name}"`;
    } catch (error) {
        status.textContent = `❌ Error: ${error.message}`;
        console.error(error);
    }
});

// --- 4. Boot the app ---
init().catch(err => {
    document.getElementById('status').textContent = `❌ Failed to load Indigo: ${err.message}`;
    console.error(err);
});