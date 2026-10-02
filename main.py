"""MiniShipSim 的统一启动入口。"""

import argparse
from pathlib import Path

from minisim.config import DEFAULT_OUTPUT_DIR, SimulationConfig


def main(argv=None):
    parser = argparse.ArgumentParser(description="运行 MiniShipSim 仿真实验")
    parser.add_argument("mode", nargs="?", default="offline",
                        choices=["offline", "compare", "keyboard"])
    parser.add_argument("--dt", type=float, default=0.1,
                        help="离线仿真的时间步长（秒）")
    parser.add_argument("--steps", type=int, default=200,
                        help="离线仿真的步数")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
                        help="输出根目录，各模式分别存入子目录")
    parser.add_argument("--no-show", action="store_true",
                        help="保存图片但不弹出绘图窗口")
    parser.add_argument("--verbose", action="store_true",
                        help="单次运行时打印每一步的状态")
    args = parser.parse_args(argv)

    if args.mode == "keyboard":
        from minisim.interactive import main as run_keyboard
        run_keyboard()
        return

    try:
        config = SimulationConfig(dt=args.dt, steps=args.steps)
    except ValueError as error:
        parser.error(str(error))

    from minisim.experiments import compare_experiments, run_experiment

    output_dir = args.output_dir / args.mode
    if args.mode == "offline":
        run_experiment(config, output_dir=output_dir,
                       show=not args.no_show, verbose=args.verbose)
    else:
        compare_experiments(config, output_dir=output_dir,
                            show=not args.no_show)

    print(f"输出目录：{output_dir.resolve()}")


if __name__ == "__main__":
    main()
