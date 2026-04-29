---
name: matlab-plot-style
description: |
  将统一的绘图样式应用于 MATLAB 代码。触发场景：
  - 用户要求格式化/标准化 MATLAB figure 代码
  - 用户要求"统一绘图格式"、"设置绘图风格"、"MATLAB绘图设置"
  - 用户提到"matlab plot style"、"publication-ready plots"
  - 用户的 MATLAB 代码中 figure 需要规范化样式
---

# MATLAB Plot Style Skill

## 样式规范速查

### Figure 模板
```matlab
figure('Color', 'w', 'Position', [200, 100, 560, 420]);
hold on; grid on; box on;

% 配色方案（plot 前）
try
    co = colororder('gem');
catch
    co = lines(7);
end
```

### 线条/标记样式

| 参数 | 值 | 说明 |
|------|-----|------|
| LineWidth | 1.2 | 所有线条 |
| MarkerSize | 6 | 散点图 |
| MarkerFaceColor | 'none' | 标记不填充 |
| 参考线 | 'k--' | 黑色虚线 |
| 标记 | 'o', 's', '^', 'd', 'v', '<', '>' | 循环使用 |
| MarkerIndices | 稀疏标记 | 数据点密集时仅每隔N个点显示标记 |

**密集仿真点稀疏标记规则：**

当仿真数据点较多（通常 > 16 个点）时，曲线连线已经足够平滑，若每个点都显示 marker 会导致视觉拥挤且难以区分重叠的曲线。此时应仅每隔若干个点显示一个 marker，使每条曲线上约有 10–14 个标记。

实现方式：在仿真参数段定义标记间隔和索引，然后在 `plot` 中通过 `'MarkerIndices'` 指定：

```matlab
% 仿真参数段（plot 前）
num_pts = length(x_data);
marker_step = max(1, round(num_pts / 12));  % 目标约12个marker
marker_idx = 1:marker_step:num_pts;

% 绘图时
plot(x_data, y_data, '-o', 'LineWidth', 1.2, 'Color', co(1,:), ...
    'MarkerSize', 6, 'MarkerFaceColor', 'none', ...
    'MarkerIndices', marker_idx, 'DisplayName', 'NI-REPA (M=3)');
```

判断标准：
- 数据点 ≤ 16：每个点都显示 marker，**不使用** `MarkerIndices`
- 数据点 > 16：启用稀疏标记，`marker_step` 取 `round(num_pts / 12)` 附近的整数值

### 曲线类型规则

根据 DisplayName 或变量名识别：
- **理论曲线**：含"理论"、"theory"、"analytical"
- **仿真曲线**：含"仿真"、"simulation"、"sim"、"Monte Carlo"

| 场景 | 理论曲线 | 仿真曲线 |
|------|----------|----------|
| 理论+仿真同时存在 | 仅线条 `'-'` | 仅标记 `'o'` |
| 仅有仿真 | - | 线条+标记 `'-o'` |

当仿真数据点 > 16 时，无论上述哪种场景，仿真曲线均应使用 `MarkerIndices` 做稀疏标记（见"线条/标记样式"一节的密集点规则）。

**多参数组分组曲线场景：**
- 当识别到可分组的曲线结构（同一算法不同参数值、同一参数组含理论/仿真多条曲线等），**必须先询问用户**选择图例呈现方式：
  - 选项 A：**分组图例** — 同组同色，颜色方块代理 + 线型代理双列布局
  - 选项 B：**平铺图例** — 每条曲线独立标注，直接 `DisplayName` 显示完整配置
- 用户选择分组时：同一参数组的所有曲线（理论/仿真/近似等）使用相同颜色，每组参数在图例中用一个纯色方块代表，曲线类型在图例中单独用黑色样例统一说明
- 用户选择平铺时：每条曲线各自 `DisplayName` 标注完整配置（如 `NI-REPA (M=8)`），图例用 `legend('show')`

### 字体选择规则

**根据内容自动选择字体：**
- 标签 (`xlabel`, `ylabel`, `title`) 或图例中包含中文字符 → 使用 `'TimesSimSun'`
- 标签和图例均为纯英文/数学符号 → 使用 `'Times New Roman'`

**判断方法：** 检查 `xlabel`, `ylabel`, `title`, `legend` 的文本内容是否匹配中文字符（Unicode 范围 `\u4e00-\u9fff`）。

### 坐标轴设置
```matlab
% 含中文时
set(gca, 'FontName', 'TimesSimSun', 'FontSize', 12, ...
    'XColor', 'k', 'YColor', 'k', 'LineWidth', 0.8);

% 纯英文时
set(gca, 'FontName', 'Times New Roman', 'FontSize', 12, ...
    'XColor', 'k', 'YColor', 'k', 'LineWidth', 0.8);
```

### 图例
```matlab
lgd = legend('show', 'Location', 'best', 'FontSize', 11, 'Interpreter', 'tex');
% 含中文时
set(lgd, 'TextColor', 'k', 'EdgeColor', 'k', 'FontName', 'TimesSimSun');
% 纯英文时
set(lgd, 'TextColor', 'k', 'EdgeColor', 'k', 'FontName', 'Times New Roman');
```

**核心原则：DisplayName 是唯一标签来源**
- 所有标签通过 `DisplayName` 在 plot 中设置
- legend 调用仅用 `'show'` 或传递句柄，**绝不重复指定标签**
- 正确：`legend('show', ...)` 或 `legend([h1, h2], ...)`
- 错误：`legend([h1, h2], {'标签1', '标签2'}, ...)` — 重复设置

### 标签（tex 解释器）
```matlab
xlabel('{\itM}', 'Interpreter', 'tex');  % 斜体 M
ylabel('{\itS}\rm_{out}', 'Interpreter', 'tex');  % 斜体 S，正体下标 out
```

### 标题处理
- **注释掉 title**：原代码中的 title 通常用于调试或文档说明，正式图表中应注释掉
- 处理方式：在 title 行前添加 `%` 注释符号

## 应用流程

**Step 1：识别现有元素**
- 绑图函数：`plot`, `scatter`, `bar`, `semilogy`, `loglog` 等
- 标签/图例：`xlabel`, `ylabel`, `title`, `legend`
- 轴设置：`xlim`, `ylim`, `xticks`, `yticks`

**Step 2：应用样式**
- 替换 `figure()` 为标准模板
- 插入配色方案（plot 前）
- 按曲线类型规则设置线条/标记样式
- **当存在可分组的曲线结构时**：先用 `question` 工具询问用户图例呈现方式（分组 or 平铺），再按用户选择应用对应图例方案
- 检测标签/图例中是否有中文，选择对应字体
- 更新 gca、legend、xlabel/ylabel

**Step 3：保持原有**
- 不改数据、变量名、循环逻辑
- 不改绘图顺序和数据范围
- 保留用户注释和导出函数

**颜色索引超过范围时取模：**
```matlab
c = co(mod(i-1, size(co,1)) + 1, :);
```

## 特殊情况

**参考线：**
```matlab
yline(value, 'k--', 'LineWidth', 1.2, 'DisplayName', 'label');
xline(value, 'k--', 'LineWidth', 1.2, 'DisplayName', 'label');
```

**对数坐标：**
```matlab
set(gca, 'YScale', 'log');  % Y轴对数
set(gca, 'XScale', 'log', 'YScale', 'log');  % 双对数
```

**多子图：** 每个 subplot 单独设置 gca 样式，根据各自标签内容选择字体。

**仅图例项（无数据）：**
```matlab
plot(NaN, NaN, 'o', 'LineWidth', 1.2, 'MarkerFaceColor', 'none', 'DisplayName', '方法A');
```

**分组曲线（颜色方块图例）：**

此方案仅在用户选择"分组图例"时使用。当同一参数组包含多条不同类型曲线（理论/仿真/上界/近似等）时，使用纯色方块作为该组的颜色代理图例：

```matlab
% 创建颜色代理句柄（每组参数一个方块）
h_color(idx) = plot(NaN, NaN, 's', 'MarkerSize', 6, 'MarkerFaceColor', c, ...
                    'MarkerEdgeColor', c, 'LineWidth', 1.2, 'DisplayName', '参数组标签');
```

图例布局规范：
- 双列布局：左侧为参数组颜色方块，右侧为曲线类型说明
- 参数组标签清晰标注对应配置（如 $N_d=10, N_e=40$）
- 曲线类型单独使用黑色样例说明（实线/虚线/点/标记等）

示例：
```matlab
% 颜色代理（参数组）
for idx = 1:num_cases
    c = co(mod(idx-1, size(co,1)) + 1, :);
    % 绘制该组所有曲线（理论+仿真），HandleVisibility='off' 不出现在图例
    plot(x, theory(idx,:), '-', 'LineWidth', 1.2, 'Color', c, 'HandleVisibility','off');
    plot(x(1:3:end), sim(idx,1:3:end), 'o', 'LineWidth', 1.2, 'Color', c, 'HandleVisibility','off');
    % 创建颜色方块代理（DisplayName在此设置）
    h_color(idx) = plot(NaN, NaN, 's', 'MarkerSize', 6, 'MarkerFaceColor', c, ...
                        'MarkerEdgeColor', c, 'LineWidth', 1.2, 'DisplayName', sprintf('组%d', idx));
end

% 线型代理（曲线类型）
h_theory = plot(NaN, NaN, 'k-', 'LineWidth', 1.2, 'DisplayName', '理论值');
h_sim = plot(NaN, NaN, 'ko', 'LineWidth', 1.2, 'MarkerFaceColor', 'none', 'DisplayName', '仿真值');

% 合并图例（仅传句柄，自动读取DisplayName）
lgd = legend([h_color, h_theory, h_sim], 'Location', 'best', 'NumColumns', 2, 'FontSize', 11, 'Interpreter', 'tex');
% 含中文时
set(lgd, 'TextColor', 'k', 'EdgeColor', 'k', 'FontName', 'TimesSimSun');
% 纯英文时改用 'FontName', 'Times New Roman'
```

## 示例

### 示例1：含中文标签

**输入：**
```matlab
figure;
plot(x1, y1, 'r-o');
xlabel('信噪比 (dB)'); ylabel('误码率');
legend('仿真值');
```

**输出：**
```matlab
figure('Color', 'w', 'Position', [200, 100, 560, 420]);
hold on; grid on; box on;
try, co = colororder('gem'); catch, co = lines(7); end

plot(x1, y1, '-o', 'LineWidth', 1.2, 'Color', co(1,:), 'MarkerFaceColor', 'none', 'DisplayName', '仿真值');

xlabel('信噪比 (dB)', 'Interpreter', 'tex');
ylabel('误码率', 'Interpreter', 'tex');
lgd = legend('show', 'Location', 'best', 'FontSize', 11, 'Interpreter', 'tex');
set(lgd, 'TextColor', 'k', 'EdgeColor', 'k', 'FontName', 'TimesSimSun');
set(gca, 'FontName', 'TimesSimSun', 'FontSize', 12, 'XColor', 'k', 'YColor', 'k', 'LineWidth', 0.8);
```

### 示例2：纯英文标签

**输入：**
```matlab
figure;
plot(x1, y1, 'r-o');
xlabel('SNR (dB)'); ylabel('BER');
legend('Simulation');
```

**输出：**
```matlab
figure('Color', 'w', 'Position', [200, 100, 560, 420]);
hold on; grid on; box on;
try, co = colororder('gem'); catch, co = lines(7); end

plot(x1, y1, '-o', 'LineWidth', 1.2, 'Color', co(1,:), 'MarkerFaceColor', 'none', 'DisplayName', 'Simulation');

xlabel('SNR (dB)', 'interpreter', 'tex');
ylabel('BER', 'interpreter', 'tex');
lgd = legend('show', 'Location', 'best', 'FontSize', 11, 'Interpreter', 'tex');
set(lgd, 'TextColor', 'k', 'EdgeColor', 'k', 'FontName', 'Times New Roman');
set(gca, 'FontName', 'Times New Roman', 'FontSize', 12, 'XColor', 'k', 'YColor', 'k', 'LineWidth', 0.8);
```

### 示例3：密集仿真点 + 稀疏标记

当横轴采样间距较小（如每1 dB一个点），数据点远多于16个时，使用 `MarkerIndices` 仅在部分点上显示标记。

**输入：**
```matlab
Pt_dBm_range = 0:1:40;
figure;
plot(Pt_dBm_range, mnap_NI_M3, '-s');
plot(Pt_dBm_range, mnap_NI_M8, '-.s');
xlabel('发射功率 (dBm)'); ylabel('归一化接收功率');
legend('NI-REPA (M=3)', 'NI-REPA (M=8)');
```

**输出：**
```matlab
Pt_dBm_range = 0:1:40;
num_pts = length(Pt_dBm_range);
marker_step = 3;  % 每3个点显示一个marker，共约14个
marker_idx = 1:marker_step:num_pts;

figure('Color', 'w', 'Position', [200, 100, 560, 420]);
hold on; grid on; box on;
try, co = colororder('gem'); catch, co = lines(7); end

plot(Pt_dBm_range, mnap_NI_M3, '-s', 'LineWidth', 1.2, 'Color', co(1,:), ...
    'MarkerSize', 6, 'MarkerFaceColor', 'none', ...
    'MarkerIndices', marker_idx, 'DisplayName', 'NI-REPA (M=3)');
plot(Pt_dBm_range, mnap_NI_M8, '-.s', 'LineWidth', 1.2, 'Color', co(1,:), ...
    'MarkerSize', 6, 'MarkerFaceColor', 'none', ...
    'MarkerIndices', marker_idx, 'DisplayName', 'NI-REPA (M=8)');

xlabel('发射功率 (dBm)', 'Interpreter', 'tex');
ylabel('归一化接收功率', 'Interpreter', 'tex');
lgd = legend('show', 'Location', 'best', 'FontSize', 11, 'Interpreter', 'tex');
set(lgd, 'TextColor', 'k', 'EdgeColor', 'k', 'FontName', 'TimesSimSun');
set(gca, 'FontName', 'TimesSimSun', 'FontSize', 12, 'XColor', 'k', 'YColor', 'k', 'LineWidth', 0.8);
```
