clear ; close all; clc;


% --- CONFIGURACION INICIAL ---
cam = videoinput('winvideo', 1);
cam.ReturnedColorSpace = 'rgb'; % Asegurar formato RGB
    
% Configurar resolucion baja para mayor velocidad si es necesario
% cam.Resolution = '640x480';

hFig = figure('Name', 'Lab. Vision Fisica', 'Position', [100, 100, 1200, 600]);
stopButton = uicontrol('Style', 'togglebutton', 'String', 'DETENER / GUARDAR','Position', [20, 20, 150, 30]);

% Matriz sRGB a CIE XYZ (D65)
M_RGB2XYZ = [0.4124, 0.3576, 0.1805; 
             0.2126, 0.7152, 0.0722; 
             0.0193, 0.1192, 0.9505];

% Variables de control
modo_filtro = 4; % 1: Paso-Bajo, 2: Paso-Alto, 3: Ranura Vertical

while stopButton.Value == 0
    % 1. ADQUISICION
    img_rgb = getsnapshot(cam);
    img_gray = double(rgb2gray(img_rgb)) / 255; 
    [rows, cols] = size(img_gray);

    F = fftshift(fft2(img_gray));
    Espectro_Visual = log (1 + abs( F ) );
    
    % --- ACTIVIDAD 1: MEDIDOR DE ENFOQUE ---
    laplacian_kernel = [0 1 0; 1 -4 1; 0 1 0];
    bordes = conv2(img_gray, laplacian_kernel, 'same');
    metric_focus = var(bordes(:)); 
    
    % --- ACTIVIDAD 2: FOURIER ---
    F = fftshift(fft2(img_gray));
    EspectroLog = log(1 + abs(F)); 
    
    % Definicion de Mascara (Coordenadas)
    [X, Y] = meshgrid(1:cols, 1:rows);
    cx = cols/2; cy = rows/2;
    %dist_sq = (X - cx).^2 + (Y - cy).^2; circular 
    dist_sq = ((X-cx)/2).^2 + ((Y-cy)/3).^2; %elipse
    radius = 20; % Radio de corte (ajustable)
    
    % Seleccion de Filtro
    if modo_filtro == 1      % Paso-Bajo (Circular)
        mask = dist_sq <= radius^2;
    elseif modo_filtro == 2  % Paso-Alto (Circular Inverso)
        mask = dist_sq > radius^2;
    else                     % Ranura Vertical (Anisotropia)
        anchura = 10;
        mask = abs(X - cx) < anchura; 
    end
    
    % Reconstruccion
    F_filtered = F .* mask; 
    img_rec = abs(ifft2(ifftshift(F_filtered)));
    
    % --- ACTIVIDAD 3: COLOR ---
    roi = double(img_rgb(cy-10:cy+10, cx-10:cx+10, :)); % ROI Central
    mean_rgb = reshape(mean(mean(roi)), 1, 3) / 255;
    rgb_lin = mean_rgb .^ 2.2; % Linealizacion Gamma
    XYZ = (M_RGB2XYZ * rgb_lin').';
    s = sum(XYZ);
    if s > 0, x = XYZ(1)/s; y = XYZ(2)/s; else, x=0; y=0; end
    n = (x - 0.3320) / (0.1858 - y);
    CCT = 449*n^3 + 3525*n^2 + 6823.3*n + 5520.33;
    
    % --- VISUALIZACION ---
    subplot(2,3,1); imshow(img_rgb); title(sprintf('T. Color: %.0f K', CCT));
    subplot(2,3,2); imagesc(EspectroLog); axis image off; title('Espectro (FFT)');
    subplot(2,3,3); bar(metric_focus); ylim([0 0.05]); title('Varianza (Enfoque)');
    subplot(2,3,[4 5 6]); imshow(img_rec, []); title('Imagen Filtrada (Espacio Real)');
    
    drawnow;
end
% Al pulsar detener, las variables quedan en el Workspace para analizar
closepreview(cam);
delete(cam); clear cam;
fprintf('Bucle detenido. Variables listas para el informe.\n');







