define(["require", "exports", "./app", "./run_view", "./diff_view", "./table/table_view", "./charting/sample"], function (require, exports, app_1, run_view_1, diff_view_1, table_view_1, sample_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    new run_view_1.RunHandler();
    new diff_view_1.DiffHandler();
    new table_view_1.TableHandler();
    new sample_1.SampleChartHandler();
    if (document.readyState === 'complete' ||
        document.readyState === 'interactive') {
        app_1.ROUTER.start(null, false);
    }
    else {
        document.addEventListener('DOMContentLoaded', () => {
            app_1.ROUTER.start(null, false);
        });
    }
});
