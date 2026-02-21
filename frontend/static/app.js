document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('convertForm');
    const sourceFile = document.getElementById('sourceFile');
    const outputFormat = document.getElementById('outputFormat');
    const templateFile = document.getElementById('templateFile');
    const templateGroup = document.getElementById('templateGroup');
    const placeholderGroup = document.getElementById('placeholderGroup');
    const placeholderInput = document.getElementById('placeholder');
    const submitBtn = document.getElementById('submitBtn');
    const result = document.getElementById('result');
    const downloadLink = document.getElementById('downloadLink');
    const errorDiv = document.getElementById('error');
    const loadingDiv = document.getElementById('loading');

    function updateTemplateVisibility() {
        const isDocx = outputFormat.value === 'docx';
        if (isDocx) {
            templateGroup.classList.add('visible');
            templateGroup.classList.remove('hidden');
            placeholderGroup.classList.add('visible');
            placeholderGroup.classList.remove('hidden');
        } else {
            templateGroup.classList.add('hidden');
            templateGroup.classList.remove('visible');
            placeholderGroup.classList.add('hidden');
            placeholderGroup.classList.remove('visible');
        }
    }

    outputFormat.addEventListener('change', updateTemplateVisibility);
    updateTemplateVisibility();

    function showError(msg) {
        errorDiv.textContent = msg;
        errorDiv.classList.remove('hidden');
        result.classList.add('hidden');
    }

    function hideError() {
        errorDiv.classList.add('hidden');
    }

    function showResult(url, filename) {
        hideError();
        downloadLink.href = url;
        downloadLink.download = filename;
        downloadLink.textContent = `Baixar ${filename}`;
        result.classList.remove('hidden');
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();
        result.classList.add('hidden');
        loadingDiv.classList.remove('hidden');
        submitBtn.disabled = true;

        const formData = new FormData();
        formData.append('source_file', sourceFile.files[0]);
        formData.append('output_format', outputFormat.value);
        formData.append('placeholder', placeholderInput.value);

        if (outputFormat.value === 'docx' && templateFile.files.length > 0 && templateFile.files[0].size > 0) {
            formData.append('template_file', templateFile.files[0]);
        }

        try {
            const base = window.location.origin;
            const response = await fetch(`${base}/api/convert`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                let msg;
                try {
                    const errData = await response.json();
                    const detail = errData.detail;
                    msg = typeof detail === 'string'
                        ? detail
                        : Array.isArray(detail)
                            ? detail.map((e) => e.msg || JSON.stringify(e)).join('; ')
                            : null;
                } catch {
                    msg = null;
                }
                throw new Error(msg || `Erro ${response.status}: ${response.statusText}`);
            }

            const blob = await response.blob();
            const disposition = response.headers.get('Content-Disposition');
            let filename = 'output';
            if (disposition) {
                const match = disposition.match(/filename="?([^";]+)"?/);
                if (match) filename = decodeURIComponent(match[1].replace(/^"|"$/g, ''));
            }
            const ext = outputFormat.value;
            const extMap = { md: 'md', tex: 'tex' };
            const expectedExt = extMap[ext] || ext;
            if (!filename.toLowerCase().endsWith('.' + expectedExt)) {
                const baseName = sourceFile.files[0]?.name?.replace(/\.[^.]+$/, '') || 'output';
                filename = baseName + '.' + expectedExt;
            }

            const url = URL.createObjectURL(blob);
            showResult(url, filename);
        } catch (err) {
            showError(err.message || 'Erro na conversão. Verifique se o Pandoc está instalado.');
        } finally {
            loadingDiv.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });
});
