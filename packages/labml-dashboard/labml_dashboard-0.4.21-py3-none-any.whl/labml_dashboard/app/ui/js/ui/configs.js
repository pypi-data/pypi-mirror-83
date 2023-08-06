define(["require", "exports", "../lib/weya/weya", "./view_components/info_list", "./view_components/format"], function (require, exports, weya_1, info_list_1, format_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    const CONFIG_PRINT_LEN = 50;
    class ConfigsView {
        constructor(configs, common = new Set()) {
            this.onShowHideClick = (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (this.elem.classList.contains('collapsed')) {
                    this.elem.classList.remove('collapsed');
                    this.showHideBtn.textContent = 'Less...';
                }
                else {
                    this.elem.classList.add('collapsed');
                    this.showHideBtn.textContent = 'More...';
                }
                this.showHideBtn.blur();
            };
            this.configs = configs;
            this.common = common;
        }
        renderComputed(conf) {
            if (typeof conf.computed === 'string') {
                let computed = conf.computed;
                computed = computed.replace('\n', '');
                if (computed.length < CONFIG_PRINT_LEN) {
                    return computed;
                }
                else {
                    return ($) => {
                        $('span', computed.substr(0, CONFIG_PRINT_LEN) + '...', { title: computed });
                    };
                }
            }
            else {
                return format_1.formatValue(conf.computed);
            }
        }
        renderOption(conf) {
            let options = new Set();
            for (let opt of conf.options) {
                options.add(opt);
            }
            let res = {
                isCustom: false,
                isOnlyOption: false,
                value: conf.value,
                otherOptions: null,
                isDefault: false
            };
            if (options.has(conf.value)) {
                options.delete(conf.value);
                if (options.size === 0) {
                    res.isOnlyOption = true;
                    res.isDefault = true;
                }
            }
            else {
                res.isCustom = true;
                if (conf.is_explicitly_specified !== true) {
                    res.isDefault = true;
                }
            }
            if (options.size > 0) {
                res.otherOptions = ($) => {
                    for (let opt of options.keys()) {
                        if (typeof opt !== 'string') {
                            continue;
                        }
                        $('span', opt);
                    }
                };
            }
            return res;
        }
        renderConfigValue(key, conf, isCommon, $, configs) {
            let isCollapsible = false;
            let classes = ['.config'];
            let conf_modules = key.split('.');
            let prefix = '';
            let parentKey = '';
            let isParentDefault = false;
            for (let i = 0; i < conf_modules.length - 1; ++i) {
                parentKey += conf_modules[i];
                let optInfo = this.renderOption(configs[parentKey]);
                if (optInfo.isDefault) {
                    isParentDefault = true;
                }
                parentKey += '.';
                prefix += '--- ';
            }
            let parts = [['.key', prefix + conf.name]];
            if (conf.order < 0) {
                classes.push('.ignored');
                isCollapsible = true;
            }
            else {
                parts.push(['.computed', this.renderComputed(conf)]);
                let optionInfo = this.renderOption(conf);
                console.log(key, isParentDefault);
                if (optionInfo.isCustom) {
                    console.log(key, isParentDefault);
                    if (isParentDefault && !conf.is_explicitly_specified && !conf.is_hyperparam && !conf.is_hyperparam) {
                        classes.push('.only_option');
                        isCollapsible = true;
                    }
                    else {
                        classes.push('.custom');
                    }
                }
                else {
                    parts.push(['.option', conf.value]);
                    if (!conf.is_explicitly_specified && !conf.is_hyperparam && (isParentDefault || optionInfo.isOnlyOption)) {
                        classes.push('.only_option');
                        isCollapsible = true;
                    }
                    else {
                        classes.push('.picked');
                    }
                }
                if (optionInfo.otherOptions != null) {
                    parts.push(['.options', optionInfo.otherOptions]);
                }
            }
            if (isCommon) {
                classes.push('.common');
                isCollapsible = true;
            }
            if (!isCollapsible) {
                classes.push('.not_collapsible');
            }
            else {
                classes.push('.collapsible');
            }
            new info_list_1.InfoList(parts, classes.join('')).render($);
            return isCollapsible;
        }
        render() {
            let conf = this.configs.configs;
            let isCollapsible = false;
            this.elem = weya_1.Weya('div.configs', $ => {
                let keys = [];
                for (let k of Object.keys(conf)) {
                    keys.push(k);
                }
                keys.sort();
                for (let k of keys) {
                    if (this.renderConfigValue(k, conf[k], this.common.has(k), $, conf)) {
                        isCollapsible = true;
                    }
                }
                isCollapsible = false;
                if (isCollapsible) {
                    this.showHideBtn = ($('button.inline', 'More...', {
                        on: {
                            click: this.onShowHideClick
                        }
                    }));
                }
            });
            if (isCollapsible) {
                this.elem.classList.add('collapsed');
            }
            return this.elem;
        }
    }
    function renderConfigs(elem, configs, common = new Set()) {
        let view = new ConfigsView(configs, common);
        elem.appendChild(view.render());
    }
    exports.renderConfigs = renderConfigs;
});
