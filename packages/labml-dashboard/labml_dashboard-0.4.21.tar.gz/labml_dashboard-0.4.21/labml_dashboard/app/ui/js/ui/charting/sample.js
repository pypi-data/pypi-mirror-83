define(["require", "exports", "../app", "../../lib/weya/weya", "../d3"], function (require, exports, app_1, weya_1, d3_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class ChartView {
        render() {
            let bars = [50, 20, 100, 200, 30];
            let xScale = d3_1.d3.scaleLinear().domain([0, 5]).range([0, 250]);
            let axis = d3_1.d3.axisBottom()
                .scale(xScale)
                .ticks(5);
            let axisElem;
            this.elem = weya_1.Weya("div.chart", $ => {
                $('svg', { width: 252, height: 280 }, $ => {
                    $('g', { transform: 'translate(2, 245)' }, $ => {
                        for (let i = 0; i < bars.length; ++i) {
                            $('g', { transform: `translate(${xScale(i)}, 0)` }, $ => {
                                $('rect', { y: -bars[i], width: 40, height: bars[i], fill: 'red' });
                            });
                        }
                    });
                    axisElem = $('g', { transform: 'translate(2, 250)' });
                });
            });
            d3_1.d3.select(axisElem)
                .append('g')
                .call(axis);
            return this.elem;
        }
    }
    class SampleChartHandler {
        constructor() {
            this.handleSampleChart = () => {
                app_1.SCREEN.setView(new ChartView());
            };
            app_1.ROUTER.route('chart/sample', [this.handleSampleChart]);
        }
    }
    exports.SampleChartHandler = SampleChartHandler;
});
