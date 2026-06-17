
import numpy as np
import plotly.graph_objects as go


def visualize_with_cube(datasets, omega_magnitude=None, cube_scale=0.1):
    

    cube = np.array([
        [-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1],
        [-1,-1, 1], [1,-1, 1], [1,1, 1], [-1,1, 1]
    ]) * cube_scale

    cube_edges = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]

    all_plotly_frames = []
    dataset_ranges = {} 

    for name, frames in datasets.items():
        start_idx = len(all_plotly_frames)

        for frame in frames:
            Xp, Yp, Zp = frame["Xp"], frame["Yp"], frame["Zp"]
            R = np.column_stack((Xp, Yp, Zp))
            rotated_cube = cube @ R.T

            traces = []

            traces.append(go.Scatter3d(
                x=[0,Xp[0]], y=[0,Xp[1]], z=[0,Xp[2]],
                mode='lines', line=dict(color='#e74c3c', width=6), name="Body X'"
            ))
            traces.append(go.Scatter3d(
                x=[0,Yp[0]], y=[0,Yp[1]], z=[0,Yp[2]],
                mode='lines', line=dict(color='#2ecc71', width=6), name="Body Y'"
            ))
            traces.append(go.Scatter3d(
                x=[0,Zp[0]], y=[0,Zp[1]], z=[0,Zp[2]],
                mode='lines', line=dict(color='#3498db', width=6), name="Body Z'"
            ))

            for a, b in cube_edges:
                traces.append(go.Scatter3d(
                    x=[rotated_cube[a,0], rotated_cube[b,0]],
                    y=[rotated_cube[a,1], rotated_cube[b,1]],
                    z=[rotated_cube[a,2], rotated_cube[b,2]],
                    mode='lines', line=dict(color='#7f8c8d', width=2),
                    showlegend=False
                ))

            all_plotly_frames.append(go.Frame(
                data=traces,
                name=f"{name} | {frame['timestamp']}"
            ))

        end_idx = len(all_plotly_frames)
        dataset_ranges[name] = (start_idx, end_idx)

    first = all_plotly_frames[0].data
    fig = go.Figure(data=list(first), frames=all_plotly_frames)

    # Fixed LVLH reference axes - dashed, low-key, no legend clutter
    axis_len = 0.5
    for axis_vec, label in [((1,0,0), 'LVLH X'), ((0,1,0), 'LVLH Y'), ((0,0,1), 'LVLH Z')]:
        fig.add_trace(go.Scatter3d(
            x=[0, axis_vec[0]*axis_len],
            y=[0, axis_vec[1]*axis_len],
            z=[0, axis_vec[2]*axis_len],
            mode='lines+text',
            line=dict(color='#bdc3c7', width=4, dash='dash'),
            text=['', label],
            textposition='top center',
            showlegend=False,
            hoverinfo='all'
        ))

    # Slider steps for ALL frames
    all_steps = []
    for i, frame in enumerate(all_plotly_frames):
        all_steps.append(dict(
            method="animate",
            args=[[frame.name], {"mode": "immediate", "frame": {"duration": 0}, "transition": {"duration": 0}}],
            label=frame.name.split(" | ")[1] if " | " in frame.name else str(i)
        ))

    # Dataset-jump buttons (Day 1 / Day 2 / Day 3 / Telemetry)
    buttons = []
    for name, (start_idx, end_idx) in dataset_ranges.items():
        target_frame_name = all_plotly_frames[start_idx].name
        buttons.append(dict(
            label=name,
            method="animate",
            args=[[target_frame_name], {"mode": "immediate", "frame": {"duration": 0}, "transition": {"duration": 0}}]
        ))

    subtitle = ""
    if omega_magnitude is not None:
        subtitle = f"<br><sub>Mean attitude rotation rate: {np.degrees(omega_magnitude):.3f}°/s</sub>"

    fig.update_layout(
        title=f"Spacecraft Attitude Viewer{subtitle}",
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50"),

        scene=dict(
            xaxis=dict(title="X ", range=[-1, 1], showbackground=False, gridcolor='#ecf0f1'),
            yaxis=dict(title="Y ", range=[-1, 1], showbackground=False, gridcolor='#ecf0f1'),
            zaxis=dict(title="Z ", range=[-1, 1], showbackground=False, gridcolor='#ecf0f1'),
            aspectmode='cube'
        ),

        updatemenus=[dict(
            type="buttons",
            direction="left",
            x=0.5, y=1.75,
            xanchor="center",
            showactive=True,
            buttons=buttons
        )],

        sliders=[dict(
            active=0,
            steps=all_steps,
            currentvalue=dict(prefix="Timestamp: ")
        )]
    )

    fig.show()