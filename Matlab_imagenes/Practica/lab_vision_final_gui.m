function lab_vision_final_gui
    % Ventana principal con cierre seguro
    fig = uifigure('Name', 'Analizador DAQ: Visión y Control de Latencia', 'Position', [30 30 1350 950]);
    fig.CloseRequestFcn = @(src, event) deleteApp(src);

    % --- DETECCIÓN DE HARDWARE ROBUSTA ---
    adaptadorActivo = ''; dispositivosNombres = {'Sin Cámara'}; dispositivosIDs = {1};
    try
        info = imaqhwinfo;
        if ~isempty(info.InstalledAdaptors)
            adaptadorActivo = char(info.InstalledAdaptors{1}); 
            dev_info = imaqhwinfo(adaptadorActivo);
            if ~isempty(dev_info.DeviceIDs)
                dispositivosNombres = cellstr({dev_info.DeviceInfo.DeviceName});
                dispositivosIDs = {dev_info.DeviceInfo.DeviceID};
            end
        else
            adaptadorActivo = 'winvideo'; 
        end
    catch
        adaptadorActivo = 'winvideo';
    end

    % --- UI COMPONENTS (Layout ya validado) ---
    pnl = uipanel(fig, 'Title', 'Filtros y Visualización', 'Position', [20 620 280 300]);
    dropView = uidropdown(pnl, 'Position', [15 250 230 25], 'Items', {'Sin Espectros', 'Solo Original', 'Solo Filtrado', 'Ambos Espectros'}, 'ItemsData', [0, 1, 2, 3], 'Value', 3);
    dropFiltro = uidropdown(pnl, 'Position', [15 155 230 25], 'Items', {'Original', 'Suavizado (Blur)', 'Bordes (Sobel)', 'Binario'}, 'ItemsData', {'orig', 'blur', 'edge', 'bin'});
    sldParam = uislider(pnl, 'Position', [35 110 200 3], 'Limits', [0.01 1], 'Value', 0.2);
    btnStart = uibutton(fig, 'state', 'Text', 'CONECTAR CÁMARA', 'Position', [20 550 280 50], 'FontWeight', 'bold');
    btnStart.ValueChangedFcn = @(btn, ~) startStop(btn);

    pnlMetrics = uipanel(fig, 'Title', 'Rendimiento DAQ', 'Position', [20 280 280 260]);
    lblFPS = uilabel(pnlMetrics, 'Text', 'FPS INST: --', 'Position', [15 220 230 22]);
    lblFPSMean = uilabel(pnlMetrics, 'Text', 'FPS MEDIOS: --', 'Position', [15 195 230 22], 'FontWeight', 'bold', 'FontColor', [0 0.4 0.8]);
    lblTs = uilabel(pnlMetrics, 'Text', 'Periodo (Ts): -- ms', 'Position', [15 170 230 22]);
    lblTc = uilabel(pnlMetrics, 'Text', 'Cómputo (Tc): -- ms', 'Position', [15 145 230 22]);
    axLag = uiaxes(pnlMetrics, 'Position', [15 10 240 100]); axLag.Title.String = 'Carga CPU';
    axLag.XTick = []; axLag.YTick = []; hLagBar = rectangle(axLag, 'Position', [0 0 0 1], 'FaceColor', 'g');

    axT1 = uiaxes(fig, 'Position', [330 650 480 260]); axT1.Title.String = 'Original r(n,m)'; axT1.DataAspectRatio = [1 1 1];
    axT2 = uiaxes(fig, 'Position', [840 650 480 260]); axT2.Title.String = 'Filtrada y(n,m)'; axT2.DataAspectRatio = [1 1 1];
    axF1 = uiaxes(fig, 'Position', [330 360 480 260]); axF1.Title.String = 'FFT Entrada';
    axF2 = uiaxes(fig, 'Position', [840 360 480 260]); axF2.Title.String = 'FFT Salida';
    axJitter = uiaxes(fig, 'Position', [330 60 990 260]); axJitter.Title.String = 'Jitter (Variación de Ts)'; axJitter.YLim = [0 120]; grid(axJitter, 'on');

    hJitterLine = plot(axJitter, zeros(1,100), 'LineWidth', 1.2, 'Color', [0.85 0.32 0.098]);
    hMeanLine = yline(axJitter, 0, '--r', 'Media');
    deviceDrop = uidropdown(fig, 'Position', [20 900 280 25], 'Items', dispositivosNombres, 'ItemsData', dispositivosIDs);
    
    vidObj = [];

    % --- LÓGICA DE CONTROL ---
    function startStop(btn)
        if btn.Value
            try
                adaptador = char(adaptadorActivo); id = deviceDrop.Value;
                if iscell(id), id = id{1}; end
                vidObj = videoinput(adaptador, id);
                vidObj.ReturnedColorspace = 'grayscale';
                triggerconfig(vidObj, 'manual');
                start(vidObj);
                btn.Text = 'DETENER'; btn.BackgroundColor = [1 0.7 0.7];
                runVision();
            catch ME
                btn.Value = false; uialert(fig, ME.message, 'Error');
            end
        else
            btn.Text = 'CONECTAR CÁMARA'; btn.BackgroundColor = [0.96 0.96 0.96];
            % El bucle se detendrá solo al cambiar btn.Value, cleanup se llama después
        end
    end

    function runVision()
        hI1 = imagesc(axT1, zeros(100,100)); hI2 = imagesc(axT2, zeros(100,100));
        hFF1 = imagesc(axF1, zeros(100,100)); hFF2 = imagesc(axF2, zeros(100,100));
        colormap(axF1, 'hot'); colormap(axF2, 'hot'); colormap(axT1, 'gray'); colormap(axT2, 'gray');
        ts_history = zeros(1, 100);

        while btnStart.Value && ishandle(fig)
            if isempty(vidObj) || ~isvalid(vidObj), break; end % PROTECCIÓN CLAVE
            
            t_ciclo = tic;
            try
                img = getsnapshot(vidObj);
                img = im2double(img);
            catch
                break; % Si falla la captura porque el objeto se está borrando, salimos
            end
            
            t_comp_start = tic;
            val = sldParam.Value;
            switch dropFiltro.Value
                case 'orig', img_out = img;
                case 'blur', k = floor(val*40)+1; img_out = imfilter(img, ones(k)/k^2);
                case 'edge', img_out = double(edge(img, 'sobel', val*0.1));
                case 'bin', img_out = double(imbinarize(img, val));
            end
            
            % FFTs
            viewMode = dropView.Value;
            if (viewMode == 1 || viewMode == 3) && ishandle(fig)
                set(hFF1, 'CData', log(1 + abs(fftshift(fft2(img))))); axF1.Visible = 'on';
            else, axF1.Visible = 'off'; 
            end
            if (viewMode == 2 || viewMode == 3) && ishandle(fig)
                set(hFF2, 'CData', log(1 + abs(fftshift(fft2(img_out))))); axF2.Visible = 'on';
            else, axF2.Visible = 'off'; 
            end
            
            t_comp = toc(t_comp_start) * 1000;
            ts_actual = toc(t_ciclo) * 1000;
            ts_history = [ts_history(2:end), ts_actual];
            
            % Métricas
            if ishandle(fig)
                lblFPS.Text = sprintf('FPS INST: %.1f', 1000/ts_actual);
                lblFPSMean.Text = sprintf('FPS MEDIOS: %.1f', 1000/mean(ts_history(ts_history > 0)));
                lblTs.Text = sprintf('Periodo (Ts): %.1f ms', ts_actual);
                lblTc.Text = sprintf('Cómputo (Tc): %.1f ms', t_comp);
                set(hJitterLine, 'YData', ts_history);
                hMeanLine.Value = mean(ts_history);
                ratio = t_comp / ts_actual;
                hLagBar.Position = [0 0 min(ratio,1) 1];
                if ratio > 0.8, hLagBar.FaceColor = 'r'; else, hLagBar.FaceColor = 'g'; end
                set(hI1, 'CData', img); set(hI2, 'CData', img_out);
            end
            drawnow limitrate;
        end
        cleanup(); % Cerramos el objeto SOLO cuando el bucle ha terminado de verdad
    end

    function cleanup()
        if ~isempty(vidObj) && isvalid(vidObj)
            stop(vidObj);
            delete(vidObj);
            vidObj = [];
        end
    end

    function deleteApp(src)
        btnStart.Value = false; % Forzamos la salida del bucle
        drawnow;
        cleanup();
        delete(src);
    end
end